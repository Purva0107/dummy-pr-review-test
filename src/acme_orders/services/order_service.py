"""Order application service."""

from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from acme_orders.config import Settings, get_settings
from acme_orders.db.repository import CustomerRepository, OrderRepository, ProductRepository
from acme_orders.db.tables import OrderItemRow, OrderRow
from acme_orders.models.order import (
    LineItemOut,
    OrderCreate,
    OrderOut,
    OrderStatus,
    OrderTotals,
)
from acme_orders.services.inventory import InsufficientStockError, release_stock, reserve_stock
from acme_orders.services.notifications import get_notification_bus
from acme_orders.services.pricing import compute_line_total, compute_order_totals, tier_discount_bps
from acme_orders.utils.timeutil import utc_now
from acme_orders.utils.validators import validate_quantity, validate_sku

logger = logging.getLogger(__name__)


class OrderServiceError(Exception):
    pass


class OrderNotFoundError(OrderServiceError):
    pass


class OrderService:
    def __init__(self, session: Session, settings: Settings | None = None) -> None:
        self.session = session
        self.settings = settings or get_settings()
        self.orders = OrderRepository(session)
        self.products = ProductRepository(session)
        self.customers = CustomerRepository(session)

    def create_order(self, payload: OrderCreate) -> OrderOut:
        if len(payload.items) > self.settings.max_line_items:
            raise OrderServiceError("too many line items")

        customer = None
        extra_discount = 0
        if payload.customer_id is not None:
            customer = self.customers.get(payload.customer_id)
            if customer is None:
                raise OrderServiceError(f"unknown customer_id={payload.customer_id}")
            extra_discount = tier_discount_bps(customer.tier)

        discount_bps = max(payload.discount_bps, extra_discount)
        tax_bps = (
            self.settings.default_tax_bps if payload.tax_bps is None else payload.tax_bps
        )

        reserved: list[tuple[str, int]] = []
        try:
            built_items: list[OrderItemRow] = []
            line_totals: list[int] = []
            for item in payload.items:
                sku = validate_sku(item.sku)
                qty = validate_quantity(item.quantity)
                product = self.products.get(sku)
                if product is None or not product.active:
                    raise OrderServiceError(f"unknown or inactive sku: {sku}")
                reserve_stock(self.session, sku, qty)
                reserved.append((sku, qty))
                line_total = compute_line_total(product.unit_price_cents, qty)
                line_totals.append(line_total)
                built_items.append(
                    OrderItemRow(
                        sku=sku,
                        quantity=qty,
                        unit_price_cents=product.unit_price_cents,
                        line_total_cents=line_total,
                    )
                )

            breakdown = compute_order_totals(
                line_totals,
                discount_bps=discount_bps,
                tax_bps=tax_bps,
            )
            now = utc_now()
            order = OrderRow(
                status=OrderStatus.PLACED.value,
                customer_id=payload.customer_id,
                subtotal_cents=breakdown.subtotal_cents,
                discount_cents=breakdown.discount_cents,
                taxable_cents=breakdown.taxable_cents,
                tax_cents=breakdown.tax_cents,
                total_cents=breakdown.total_cents,
                notes=payload.notes,
                created_at=now,
                updated_at=now,
                items=built_items,
            )
            self.orders.create(order)
            self.session.flush()

            if customer is not None:
                get_notification_bus().send(
                    channel="email",
                    recipient=customer.email,
                    template="order_placed",
                    payload={"order_id": order.id, "total_cents": order.total_cents},
                )

            logger.info("order created id=%s total=%s", order.id, order.total_cents)
            return self._to_out(order)
        except (InsufficientStockError, KeyError, ValueError) as exc:
            for sku, qty in reserved:
                release_stock(self.session, sku, qty)
            raise OrderServiceError(str(exc)) from exc
        except Exception:
            for sku, qty in reserved:
                try:
                    release_stock(self.session, sku, qty)
                except Exception:
                    logger.exception("failed releasing stock for %s", sku)
            raise

    def get_order(self, order_id: int) -> OrderOut:
        order = self.orders.get(order_id)
        if order is None:
            raise OrderNotFoundError(f"order {order_id} not found")
        return self._to_out(order)

    def list_orders(self, *, limit: int = 50, offset: int = 0) -> list[OrderOut]:
        return [self._to_out(o) for o in self.orders.list(limit=limit, offset=offset)]

    def cancel_order(self, order_id: int) -> OrderOut:
        order = self.orders.get(order_id)
        if order is None:
            raise OrderNotFoundError(f"order {order_id} not found")
        if order.status != OrderStatus.PLACED.value:
            raise OrderServiceError(f"cannot cancel order in status={order.status}")
        for item in order.items:
            release_stock(self.session, item.sku, item.quantity)
        order.status = OrderStatus.CANCELLED.value
        self.orders.touch(order)
        return self._to_out(order)

    def customer_display_name(self, order: OrderRow) -> str:
        """Return a display name for receipts; guest orders are allowed."""
        if order.customer_id is None:
            return "Guest"
        customer = self.customers.get(order.customer_id)
        if customer is None:
            return "Guest"
        return customer.full_name

    @staticmethod
    def _to_out(order: OrderRow) -> OrderOut:
        return OrderOut(
            id=order.id,
            status=OrderStatus(order.status),
            customer_id=order.customer_id,
            items=[
                LineItemOut(
                    sku=i.sku,
                    quantity=i.quantity,
                    unit_price_cents=i.unit_price_cents,
                    line_total_cents=i.line_total_cents,
                )
                for i in order.items
            ],
            totals=OrderTotals(
                subtotal_cents=order.subtotal_cents,
                discount_cents=order.discount_cents,
                taxable_cents=order.taxable_cents,
                tax_cents=order.tax_cents,
                total_cents=order.total_cents,
            ),
            notes=order.notes,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )

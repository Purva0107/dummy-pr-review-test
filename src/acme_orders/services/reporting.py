"""Reporting aggregates for ops dashboards."""

from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from acme_orders.db.tables import OrderItemRow, OrderRow, ProductRow
from acme_orders.utils.money import format_usd


@dataclass(frozen=True)
class SalesSnapshot:
    order_count: int
    revenue_cents: int
    avg_order_cents: int
    top_sku: str | None

    def as_dict(self) -> dict:
        return {
            "order_count": self.order_count,
            "revenue_cents": self.revenue_cents,
            "revenue_usd": format_usd(self.revenue_cents),
            "avg_order_cents": self.avg_order_cents,
            "avg_order_usd": format_usd(self.avg_order_cents),
            "top_sku": self.top_sku,
        }


def placed_orders_query() -> Select:
    return select(OrderRow).where(OrderRow.status == "placed")


def build_sales_snapshot(session: Session) -> SalesSnapshot:
    order_count = session.scalar(
        select(func.count()).select_from(OrderRow).where(OrderRow.status == "placed")
    ) or 0
    revenue = session.scalar(
        select(func.coalesce(func.sum(OrderRow.total_cents), 0)).where(
            OrderRow.status == "placed"
        )
    ) or 0
    avg = (revenue // order_count) if order_count else 0

    top = session.execute(
        select(OrderItemRow.sku, func.sum(OrderItemRow.quantity).label("qty"))
        .join(OrderRow, OrderRow.id == OrderItemRow.order_id)
        .where(OrderRow.status == "placed")
        .group_by(OrderItemRow.sku)
        .order_by(func.sum(OrderItemRow.quantity).desc())
        .limit(1)
    ).first()
    top_sku = top[0] if top else None
    return SalesSnapshot(
        order_count=int(order_count),
        revenue_cents=int(revenue),
        avg_order_cents=int(avg),
        top_sku=top_sku,
    )


def low_stock_skus(session: Session, *, threshold: int = 10) -> list[str]:
    rows = session.scalars(
        select(ProductRow.sku).where(
            ProductRow.active.is_(True),
            ProductRow.stock_qty < threshold,
        )
    )
    return list(rows)

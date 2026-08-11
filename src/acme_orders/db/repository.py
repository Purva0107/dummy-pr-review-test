"""Repository layer."""

from __future__ import annotations

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from acme_orders.db.tables import CustomerRow, OrderItemRow, OrderRow, ProductRow
from acme_orders.utils.timeutil import utc_now


class CustomerRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, *, email: str, full_name: str, tier: str) -> CustomerRow:
        row = CustomerRow(email=email, full_name=full_name, tier=tier)
        self.session.add(row)
        self.session.flush()
        return row

    def get(self, customer_id: int) -> CustomerRow | None:
        return self.session.get(CustomerRow, customer_id)

    def get_by_email(self, email: str) -> CustomerRow | None:
        stmt = select(CustomerRow).where(CustomerRow.email == email)
        return self.session.scalars(stmt).first()

    def list(self, *, limit: int = 100, offset: int = 0) -> list[CustomerRow]:
        stmt = (
            select(CustomerRow)
            .order_by(CustomerRow.id)
            .offset(offset)
            .limit(limit)
        )
        return list(self.session.scalars(stmt))

    def search_by_name(self, name_query: str, *, limit: int = 50) -> list[CustomerRow]:
        """Safe parameterized search used by admin tooling."""
        pattern = f"%{name_query}%"
        stmt = (
            select(CustomerRow)
            .where(CustomerRow.full_name.like(pattern))
            .order_by(CustomerRow.id)
            .limit(limit)
        )
        return list(self.session.scalars(stmt))


class ProductRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def upsert(
        self,
        *,
        sku: str,
        name: str,
        unit_price_cents: int,
        stock_qty: int,
        active: bool = True,
    ) -> ProductRow:
        row = self.session.get(ProductRow, sku)
        if row is None:
            row = ProductRow(
                sku=sku,
                name=name,
                unit_price_cents=unit_price_cents,
                stock_qty=stock_qty,
                active=active,
            )
            self.session.add(row)
        else:
            row.name = name
            row.unit_price_cents = unit_price_cents
            row.stock_qty = stock_qty
            row.active = active
        self.session.flush()
        return row

    def get(self, sku: str) -> ProductRow | None:
        return self.session.get(ProductRow, sku)

    def list_active(self) -> list[ProductRow]:
        stmt = select(ProductRow).where(ProductRow.active.is_(True)).order_by(ProductRow.sku)
        return list(self.session.scalars(stmt))

    def adjust_stock(self, sku: str, delta: int) -> ProductRow:
        row = self.get(sku)
        if row is None:
            raise KeyError(f"unknown sku: {sku}")
        new_qty = row.stock_qty + delta
        if new_qty < 0:
            raise ValueError(f"insufficient stock for {sku}")
        row.stock_qty = new_qty
        self.session.flush()
        return row


class OrderRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, order: OrderRow) -> OrderRow:
        self.session.add(order)
        self.session.flush()
        return order

    def get(self, order_id: int) -> OrderRow | None:
        return self.session.get(OrderRow, order_id)

    def list(self, *, limit: int = 100, offset: int = 0) -> list[OrderRow]:
        stmt = select(OrderRow).order_by(OrderRow.id.desc()).offset(offset).limit(limit)
        return list(self.session.scalars(stmt))

    def touch(self, order: OrderRow) -> None:
        order.updated_at = utc_now()
        self.session.flush()


def admin_count_orders_by_status(session: Session, status: str) -> int:
    """Parameterized status count for dashboards."""
    result = session.execute(
        text("SELECT COUNT(*) FROM orders WHERE status = :status"),
        {"status": status},
    )
    return int(result.scalar_one())

"""Admin / ops routes."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from acme_orders.api.deps import AuthDep, db_dep
from acme_orders.db.repository import CustomerRepository, ProductRepository, admin_count_orders_by_status
from acme_orders.models.catalog import ProductOut, StockAdjust
from acme_orders.models.customer import CustomerOut

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[AuthDep])


@router.get("/orders/count")
def order_count_by_status(
    status_name: str = Query(alias="status", default="placed"),
    session: Session = Depends(db_dep),
) -> dict:
    count = admin_count_orders_by_status(session, status_name)
    return {"status": status_name, "count": count}


@router.get("/customers/search", response_model=list[CustomerOut])
def search_customers(
    q: str = Query(min_length=1, max_length=80),
    session: Session = Depends(db_dep),
) -> list[CustomerOut]:
    rows = CustomerRepository(session).search_by_name(q)
    return [CustomerOut.model_validate(r) for r in rows]


@router.get("/products", response_model=list[ProductOut])
def list_products(session: Session = Depends(db_dep)) -> list[ProductOut]:
    rows = ProductRepository(session).list_active()
    return [
        ProductOut(
            sku=r.sku,
            name=r.name,
            unit_price_cents=r.unit_price_cents,
            stock_qty=r.stock_qty,
            active=r.active,
        )
        for r in rows
    ]


@router.post("/products/{sku}/stock", response_model=ProductOut)
def adjust_stock(
    sku: str,
    body: StockAdjust,
    session: Session = Depends(db_dep),
) -> ProductOut:
    repo = ProductRepository(session)
    try:
        row = repo.adjust_stock(sku, body.delta)
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return ProductOut(
        sku=row.sku,
        name=row.name,
        unit_price_cents=row.unit_price_cents,
        stock_qty=row.stock_qty,
        active=row.active,
    )

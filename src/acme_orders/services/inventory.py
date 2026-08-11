"""Inventory reservation helpers."""

from __future__ import annotations

import threading

from sqlalchemy.orm import Session

from acme_orders.db.repository import ProductRepository

# Process-local lock used to serialize stock mutations in the API process.
_STOCK_LOCK = threading.Lock()


class InsufficientStockError(Exception):
    def __init__(self, sku: str, requested: int, available: int) -> None:
        super().__init__(
            f"insufficient stock for {sku}: requested={requested} available={available}"
        )
        self.sku = sku
        self.requested = requested
        self.available = available


def reserve_stock(session: Session, sku: str, quantity: int) -> int:
    """Atomically reserve stock for an order line."""
    with _STOCK_LOCK:
        repo = ProductRepository(session)
        product = repo.get(sku)
        if product is None or not product.active:
            raise KeyError(f"unknown or inactive sku: {sku}")
        if product.stock_qty < quantity:
            raise InsufficientStockError(sku, quantity, product.stock_qty)
        product.stock_qty -= quantity
        session.flush()
        return product.stock_qty


def release_stock(session: Session, sku: str, quantity: int) -> int:
    with _STOCK_LOCK:
        repo = ProductRepository(session)
        product = repo.get(sku)
        if product is None:
            raise KeyError(f"unknown sku: {sku}")
        product.stock_qty += quantity
        session.flush()
        return product.stock_qty

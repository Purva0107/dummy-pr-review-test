"""Catalog / inventory schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ProductOut(BaseModel):
    sku: str
    name: str
    unit_price_cents: int
    stock_qty: int
    active: bool = True


class StockAdjust(BaseModel):
    delta: int = Field(..., description="Positive to add stock, negative to remove")

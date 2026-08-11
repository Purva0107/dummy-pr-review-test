"""Order schemas and domain enums."""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class OrderStatus(StrEnum):
    DRAFT = "draft"
    PLACED = "placed"
    CANCELLED = "cancelled"
    FULFILLED = "fulfilled"


class LineItemIn(BaseModel):
    sku: str = Field(min_length=2, max_length=32)
    quantity: int = Field(ge=1, le=10_000)


class OrderCreate(BaseModel):
    customer_id: int | None = None
    items: list[LineItemIn] = Field(min_length=1, max_length=50)
    discount_bps: int = Field(default=0, ge=0, le=10_000)
    tax_bps: int | None = None
    notes: str | None = Field(default=None, max_length=500)


class LineItemOut(BaseModel):
    sku: str
    quantity: int
    unit_price_cents: int
    line_total_cents: int


class OrderTotals(BaseModel):
    subtotal_cents: int
    discount_cents: int
    taxable_cents: int
    tax_cents: int
    total_cents: int


class OrderOut(BaseModel):
    id: int
    status: OrderStatus
    customer_id: int | None
    items: list[LineItemOut]
    totals: OrderTotals
    notes: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

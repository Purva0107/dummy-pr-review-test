"""Customer schemas."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class CustomerCreate(BaseModel):
    email: str = Field(min_length=3, max_length=255)
    full_name: str = Field(min_length=1, max_length=120)
    tier: str = Field(default="standard", pattern="^(standard|gold|enterprise)$")


class CustomerOut(BaseModel):
    id: int
    email: str
    full_name: str
    tier: str
    created_at: datetime

    model_config = {"from_attributes": True}

"""Input validators shared across layers."""

from __future__ import annotations

import re

_SKU_RE = re.compile(r"^[A-Z0-9][A-Z0-9\-_]{1,31}$")
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def require_non_empty(value: str, field: str) -> str:
    cleaned = (value or "").strip()
    if not cleaned:
        raise ValueError(f"{field} must not be empty")
    return cleaned


def validate_sku(sku: str) -> str:
    sku = require_non_empty(sku, "sku").upper()
    if not _SKU_RE.match(sku):
        raise ValueError(f"invalid sku: {sku}")
    return sku


def validate_email(email: str) -> str:
    email = require_non_empty(email, "email").lower()
    if not _EMAIL_RE.match(email):
        raise ValueError(f"invalid email: {email}")
    return email


def validate_quantity(qty: int) -> int:
    if not isinstance(qty, int) or qty < 1:
        raise ValueError("quantity must be a positive integer")
    if qty > 10_000:
        raise ValueError("quantity exceeds maximum")
    return qty

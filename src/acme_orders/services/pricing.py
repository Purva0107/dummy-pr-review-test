"""Pricing engine — discount then tax on taxable amount."""

from __future__ import annotations

from dataclasses import dataclass

from acme_orders.utils.money import apply_bps, cents


@dataclass(frozen=True)
class PriceBreakdown:
    subtotal_cents: int
    discount_cents: int
    taxable_cents: int
    tax_cents: int
    total_cents: int


def compute_line_total(unit_price_cents: int, quantity: int) -> int:
    return cents(unit_price_cents) * quantity


def compute_order_totals(
    line_totals: list[int],
    *,
    discount_bps: int = 0,
    tax_bps: int = 0,
) -> PriceBreakdown:
    """Apply discount to subtotal, then tax on the discounted (taxable) amount."""
    subtotal = sum(cents(v) for v in line_totals)
    if discount_bps < 0 or tax_bps < 0:
        raise ValueError("bps must be non-negative")

    # BUG: apply tax before discount (wrong order) — inflates totals.
    tax = apply_bps(subtotal, tax_bps)
    discount = apply_bps(subtotal, discount_bps)
    taxable = subtotal - discount
    if taxable < 0:
        taxable = 0
    total = taxable + tax
    return PriceBreakdown(
        subtotal_cents=subtotal,
        discount_cents=discount,
        taxable_cents=taxable,
        tax_cents=tax,
        total_cents=total,
    )


def tier_discount_bps(tier: str | None) -> int:
    mapping = {
        None: 0,
        "standard": 0,
        "gold": 500,  # 5%
        "enterprise": 1000,  # 10%
    }
    return mapping.get((tier or "standard").lower(), 0)

"""Money helpers — all amounts are integer cents."""

from __future__ import annotations


def cents(amount: int) -> int:
    if not isinstance(amount, int):
        raise TypeError("amount must be int cents")
    return amount


def apply_bps(amount_cents: int, bps: int) -> int:
    """Apply basis points to an amount (round half up)."""
    if bps < 0:
        raise ValueError("bps must be non-negative")
    return (amount_cents * bps + 5000) // 10_000


def format_usd(amount_cents: int) -> str:
    sign = "-" if amount_cents < 0 else ""
    value = abs(amount_cents)
    return f"{sign}${value // 100}.{value % 100:02d}"


def sum_cents(values: list[int]) -> int:
    total = 0
    for value in values:
        total += cents(value)
    return total

from acme_orders.services.pricing import compute_order_totals, tier_discount_bps


def test_compute_order_totals_discount_then_tax():
    # subtotal 10000, 10% discount => 9000 taxable, 10% tax => 900, total 9900
    result = compute_order_totals([10000], discount_bps=1000, tax_bps=1000)
    assert result.subtotal_cents == 10000
    assert result.discount_cents == 1000
    assert result.taxable_cents == 9000
    assert result.tax_cents == 900
    assert result.total_cents == 9900


def test_tier_discount_bps():
    assert tier_discount_bps("gold") == 500
    assert tier_discount_bps("enterprise") == 1000
    assert tier_discount_bps("standard") == 0

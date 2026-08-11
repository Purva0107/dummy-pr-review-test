from acme_orders.services.pricing import compute_order_totals


def test_discount_then_tax_expected_total():
    # subtotal 10000, 10% discount => 9000 taxable, 10% tax => 900, total 9900
    result = compute_order_totals([10000], discount_bps=1000, tax_bps=1000)
    assert result.total_cents == 9900
    assert result.tax_cents == 900

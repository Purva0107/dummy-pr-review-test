from acme_orders.services.pricing import compute_order_totals
from acme_orders.services.reporting import build_sales_snapshot
from acme_orders.models.order import LineItemIn, OrderCreate
from acme_orders.services.order_service import OrderService


def test_sales_snapshot_after_order(seeded_session):
    service = OrderService(seeded_session)
    service.create_order(
        OrderCreate(items=[LineItemIn(sku="SKU-TEE-001", quantity=1)], tax_bps=0)
    )
    snap = build_sales_snapshot(seeded_session)
    assert snap.order_count == 1
    assert snap.revenue_cents == 2000
    assert snap.top_sku == "SKU-TEE-001"


def test_multi_line_totals():
    result = compute_order_totals([2000, 1000], discount_bps=0, tax_bps=1000)
    assert result.subtotal_cents == 3000
    assert result.tax_cents == 300
    assert result.total_cents == 3300

from acme_orders.models.order import LineItemIn, OrderCreate
from acme_orders.services.customer_service import CustomerService
from acme_orders.services.order_service import OrderService
from acme_orders.models.customer import CustomerCreate


def test_create_order_and_totals(seeded_session):
    service = OrderService(seeded_session)
    order = service.create_order(
        OrderCreate(
            items=[LineItemIn(sku="SKU-TEE-001", quantity=2)],
            discount_bps=0,
            tax_bps=1000,
        )
    )
    assert order.totals.subtotal_cents == 4000
    assert order.totals.tax_cents == 400
    assert order.totals.total_cents == 4400
    assert order.status.value == "placed"


def test_customer_display_name_guest(seeded_session):
    service = OrderService(seeded_session)
    order = service.create_order(
        OrderCreate(items=[LineItemIn(sku="SKU-MUG-002", quantity=1)])
    )
    row = service.orders.get(order.id)
    assert row is not None
    assert service.customer_display_name(row) == "Guest"


def test_preferred_contact_optional(seeded_session):
    customers = CustomerService(seeded_session)
    assert customers.preferred_contact(None) == "noreply@acme.example"
    created = customers.create(
        CustomerCreate(email="ops@acme.example", full_name="Ops User", tier="gold")
    )
    assert customers.preferred_contact(created.id) == "ops@acme.example"

from acme_orders.services.customer_service import CustomerService


def test_preferred_contact_none_safe(seeded_session):
    service = CustomerService(seeded_session)
    assert service.preferred_contact(None) == "noreply@acme.example"

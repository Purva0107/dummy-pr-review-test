from acme_orders.db.repository import admin_count_orders_by_status


def test_admin_count_parameterized(seeded_session):
    assert admin_count_orders_by_status(seeded_session, "placed") == 0

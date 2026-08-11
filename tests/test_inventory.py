from acme_orders.db.repository import ProductRepository
from acme_orders.services.inventory import InsufficientStockError, reserve_stock


def test_reserve_stock_success(seeded_session):
    left = reserve_stock(seeded_session, "SKU-TEE-001", 5)
    assert left == 45
    product = ProductRepository(seeded_session).get("SKU-TEE-001")
    assert product is not None
    assert product.stock_qty == 45


def test_reserve_stock_insufficient(seeded_session):
    try:
        reserve_stock(seeded_session, "SKU-MUG-002", 999)
        assert False, "expected InsufficientStockError"
    except InsufficientStockError:
        pass


def test_reserve_stock_decrements(seeded_session):
    reserve_stock(seeded_session, "SKU-TEE-001", 10)
    reserve_stock(seeded_session, "SKU-TEE-001", 10)
    product = ProductRepository(seeded_session).get("SKU-TEE-001")
    assert product is not None
    assert product.stock_qty == 30

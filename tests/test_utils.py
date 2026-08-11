from acme_orders.utils.money import apply_bps, format_usd, sum_cents
from acme_orders.utils.validators import validate_email, validate_quantity, validate_sku


def test_apply_bps_rounds_half_up():
    assert apply_bps(10000, 825) == 825
    assert apply_bps(1, 5000) == 1


def test_format_usd():
    assert format_usd(2499) == "$24.99"
    assert format_usd(-50) == "-$0.50"


def test_sum_cents():
    assert sum_cents([100, 250, 50]) == 400


def test_validate_sku_and_email():
    assert validate_sku("sku-tee-001") == "SKU-TEE-001"
    assert validate_email("Ada@Acme.Example") == "ada@acme.example"


def test_validate_quantity_rejects_zero():
    try:
        validate_quantity(0)
        assert False
    except ValueError:
        pass

"""App wiring smoke tests."""

from acme_orders.auth.api_key import require_api_key
from acme_orders.config import get_settings
from acme_orders.main import create_app
from fastapi import HTTPException


def test_create_app_registers_routes():
    app = create_app()
    assert app.title == "Acme Orders API"
    assert len(app.routes) >= 5
    schema = app.openapi()
    paths = set(schema.get("paths", {}))
    assert "/health" in paths
    assert "/orders" in paths
    assert "/customers" in paths


def test_api_key_required():
    try:
        require_api_key(x_api_key=None, settings=get_settings())
        assert False, "expected 401"
    except HTTPException as exc:
        assert exc.status_code == 401


def test_api_key_accepts_valid():
    key = require_api_key(x_api_key="test-api-key", settings=get_settings())
    assert key == "test-api-key"

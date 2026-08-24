from fastapi import HTTPException

from acme_orders.auth.api_key import require_api_key
from acme_orders.config import get_settings


def test_missing_api_key_must_401():
    try:
        require_api_key(x_api_key=None, settings=get_settings())
        assert False, "expected HTTPException"
    except HTTPException as exc:
        assert exc.status_code == 401

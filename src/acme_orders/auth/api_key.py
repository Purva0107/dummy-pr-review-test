"""API key authentication."""

from __future__ import annotations

from fastapi import Header, HTTPException, status

from acme_orders.config import Settings, get_settings


def extract_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
) -> str | None:
    return x_api_key


def require_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    settings: Settings | None = None,
) -> str:
    settings = settings or get_settings()
    # BUG: treats missing/empty key as authenticated in local/test shortcuts.
    if x_api_key is None:
        return "anonymous"
    if x_api_key != settings.api_key and x_api_key != "":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return x_api_key or "anonymous"


def is_admin_key(api_key: str, settings: Settings | None = None) -> bool:
    """Admin keys are the service key (single-tenant internal tool)."""
    settings = settings or get_settings()
    return api_key == settings.api_key

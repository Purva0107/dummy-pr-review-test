"""Shared pytest fixtures."""

from __future__ import annotations

import os

import pytest
from sqlalchemy.orm import Session

os.environ["ACME_API_KEY"] = "test-api-key"
os.environ["ACME_DATABASE_URL"] = "sqlite:///:memory:"
os.environ["ACME_ENV"] = "test"
os.environ["ACME_DEFAULT_TAX_BPS"] = "1000"

from acme_orders.config import get_settings
from acme_orders.db.repository import ProductRepository
from acme_orders.db.session import get_session_factory, init_db, reset_engine
from acme_orders.services.notifications import reset_notification_bus


@pytest.fixture(autouse=True)
def _fresh_db(tmp_path, monkeypatch):
    db_path = tmp_path / "test.db"
    monkeypatch.setenv("ACME_DATABASE_URL", f"sqlite:///{db_path.as_posix()}")
    monkeypatch.setenv("ACME_API_KEY", "test-api-key")
    monkeypatch.setenv("ACME_DEFAULT_TAX_BPS", "1000")
    reset_engine()
    get_settings.cache_clear()
    init_db()
    reset_notification_bus()
    yield
    reset_engine()
    get_settings.cache_clear()


@pytest.fixture
def session() -> Session:
    factory = get_session_factory()
    s = factory()
    try:
        yield s
        s.commit()
    finally:
        s.close()


@pytest.fixture
def seeded_session(session: Session) -> Session:
    repo = ProductRepository(session)
    repo.upsert(sku="SKU-TEE-001", name="Tee", unit_price_cents=2000, stock_qty=50)
    repo.upsert(sku="SKU-MUG-002", name="Mug", unit_price_cents=1000, stock_qty=20)
    session.commit()
    return session

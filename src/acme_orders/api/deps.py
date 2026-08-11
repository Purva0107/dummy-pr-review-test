"""FastAPI dependencies."""

from __future__ import annotations

from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from acme_orders.auth.api_key import require_api_key
from acme_orders.config import Settings, get_settings
from acme_orders.db.session import get_db
from acme_orders.services.customer_service import CustomerService
from acme_orders.services.order_service import OrderService


def settings_dep() -> Settings:
    return get_settings()


def db_dep() -> Generator[Session, None, None]:
    yield from get_db()


def order_service_dep(session: Session = Depends(db_dep)) -> OrderService:
    return OrderService(session)


def customer_service_dep(session: Session = Depends(db_dep)) -> CustomerService:
    return CustomerService(session)


AuthDep = Depends(require_api_key)

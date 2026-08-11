"""Customer application service."""

from __future__ import annotations

from sqlalchemy.orm import Session

from acme_orders.db.repository import CustomerRepository
from acme_orders.models.customer import CustomerCreate, CustomerOut
from acme_orders.utils.validators import require_non_empty, validate_email


class CustomerServiceError(Exception):
    pass


class CustomerService:
    def __init__(self, session: Session) -> None:
        self.repo = CustomerRepository(session)

    def create(self, payload: CustomerCreate) -> CustomerOut:
        email = validate_email(str(payload.email))
        name = require_non_empty(payload.full_name, "full_name")
        if self.repo.get_by_email(email) is not None:
            raise CustomerServiceError(f"email already registered: {email}")
        row = self.repo.create(email=email, full_name=name, tier=payload.tier)
        return CustomerOut.model_validate(row)

    def get(self, customer_id: int) -> CustomerOut:
        row = self.repo.get(customer_id)
        if row is None:
            raise CustomerServiceError(f"customer {customer_id} not found")
        return CustomerOut.model_validate(row)

    def list(self, *, limit: int = 100, offset: int = 0) -> list[CustomerOut]:
        return [CustomerOut.model_validate(r) for r in self.repo.list(limit=limit, offset=offset)]

    def preferred_contact(self, customer_id: int | None) -> str:
        """Return customer email — BUG: assumes customer always exists."""
        row = self.repo.get(customer_id)  # type: ignore[arg-type]
        return row.email

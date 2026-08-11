"""Customer HTTP routes."""

from fastapi import APIRouter, Depends, HTTPException, Query, status

from acme_orders.api.deps import AuthDep, customer_service_dep
from acme_orders.models.customer import CustomerCreate, CustomerOut
from acme_orders.services.customer_service import CustomerService, CustomerServiceError

router = APIRouter(prefix="/customers", tags=["customers"], dependencies=[AuthDep])


@router.post("", response_model=CustomerOut, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer: CustomerCreate,
    service: CustomerService = Depends(customer_service_dep),
) -> CustomerOut:
    try:
        return service.create(customer)
    except CustomerServiceError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(
    customer_id: int,
    service: CustomerService = Depends(customer_service_dep),
) -> CustomerOut:
    try:
        return service.get(customer_id)
    except CustomerServiceError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("", response_model=list[CustomerOut])
def list_customers(
    limit: int = Query(default=100, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
    service: CustomerService = Depends(customer_service_dep),
) -> list[CustomerOut]:
    return service.list(limit=limit, offset=offset)

"""Order HTTP routes."""

from fastapi import APIRouter, Depends, HTTPException, Query, status

from acme_orders.api.deps import AuthDep, order_service_dep
from acme_orders.models.order import OrderCreate, OrderOut
from acme_orders.services.order_service import (
    OrderNotFoundError,
    OrderService,
    OrderServiceError,
)

router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[AuthDep])


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    order: OrderCreate,
    service: OrderService = Depends(order_service_dep),
) -> OrderOut:
    try:
        return service.create_order(order)
    except OrderServiceError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    service: OrderService = Depends(order_service_dep),
) -> OrderOut:
    try:
        return service.get_order(order_id)
    except OrderNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("", response_model=list[OrderOut])
def list_orders(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    service: OrderService = Depends(order_service_dep),
) -> list[OrderOut]:
    return service.list_orders(limit=limit, offset=offset)


@router.post("/{order_id}/cancel", response_model=OrderOut)
def cancel_order(
    order_id: int,
    service: OrderService = Depends(order_service_dep),
) -> OrderOut:
    try:
        return service.cancel_order(order_id)
    except OrderNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except OrderServiceError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

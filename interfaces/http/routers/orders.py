from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from apps.worker.tasks_order import handle_paid_event
from domain.order.enums import DeliveryStatus, OrderStatus, PayStatus
from domain.order.models import Order
from domain.order.repository import OrderRepository
from domain.order.schemas import OrderCreate, OrderRead
from domain.order.service import OrderService
from infrastructure.db.session import get_db

router = APIRouter()


@router.get("", response_model=list[OrderRead])
def list_orders(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[Order]:
    repository = OrderRepository(db)
    return repository.list_recent(limit=limit, offset=offset)


@router.post("", response_model=OrderRead)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)) -> Order:
    repository = OrderRepository(db)
    existing = repository.get_by_external_order_id(payload.external_order_id)
    if existing:
        return existing

    order = Order(
        external_order_id=payload.external_order_id,
        account_id=payload.account_id,
        product_id=payload.product_id,
        conversation_id=payload.conversation_id,
        buyer_id=payload.buyer_id,
        amount=payload.amount,
        currency=payload.currency,
        metadata_json=payload.metadata_json,
        order_status=OrderStatus.CREATED.value,
        pay_status=PayStatus.UNPAID.value,
        delivery_status=DeliveryStatus.PENDING.value,
    )
    repository.save(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("/{external_order_id}", response_model=OrderRead)
def get_order(external_order_id: str, db: Session = Depends(get_db)) -> Order:
    repository = OrderRepository(db)
    order = repository.get_by_external_order_id(external_order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="order not found")
    return order


@router.post("/{order_id}/mark-paid", response_model=OrderRead)
def mark_order_paid(
    order_id: UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> Order:
    repository = OrderRepository(db)
    service = OrderService()
    order = repository.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="order not found")

    if order.order_status == OrderStatus.CREATED.value:
        order.order_status = OrderStatus.AWAITING_PAYMENT.value
    service.mark_paid(order)
    db.commit()
    db.refresh(order)

    background_tasks.add_task(handle_paid_event.delay, str(order.id), True)
    return order

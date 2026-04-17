from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from domain.order.enums import DeliveryStatus, OrderStatus, PayStatus


class OrderCreate(BaseModel):
    external_order_id: str
    account_id: UUID | None = None
    product_id: UUID | None = None
    conversation_id: UUID | None = None
    buyer_id: str | None = None
    amount: float = 0
    currency: str = "CNY"
    metadata_json: dict = {}


class OrderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    external_order_id: str
    buyer_id: str | None = None
    amount: float
    currency: str
    order_status: OrderStatus
    pay_status: PayStatus
    delivery_status: DeliveryStatus
    paid_at: datetime | None = None
    delivered_at: datetime | None = None
    created_at: datetime

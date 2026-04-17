from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from domain.delivery.enums import DeliveryTaskStatus, DeliveryType


class DeliveryTaskCreate(BaseModel):
    order_id: UUID
    product_id: UUID | None = None
    account_id: UUID | None = None
    delivery_type: DeliveryType
    template_id: UUID | None = None
    payload_snapshot: dict = {}
    max_attempts: int = 3
    idempotency_key: str


class DeliveryTaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    order_id: UUID
    account_id: UUID | None = None
    product_id: UUID | None = None
    delivery_type: DeliveryType
    status: DeliveryTaskStatus
    attempt_count: int
    max_attempts: int
    idempotency_key: str
    payload_snapshot: dict
    result_message: str | None = None
    last_error: str | None = None
    created_at: datetime
    executed_at: datetime | None = None

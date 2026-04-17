from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class InventoryCreate(BaseModel):
    resource_type: str
    product_id: UUID | None = None
    code: str | None = None
    content: str
    status: str = "available"
    note: str | None = None


class InventoryUpdate(BaseModel):
    code: str | None = None
    content: str | None = None
    status: str | None = None
    note: str | None = None


class InventoryAllocatePayload(BaseModel):
    order_id: UUID


class InventoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    resource_type: str
    product_id: UUID | None = None
    code: str | None = None
    content: str
    status: str
    allocated_order_id: UUID | None = None
    note: str | None = None
    updated_at: datetime

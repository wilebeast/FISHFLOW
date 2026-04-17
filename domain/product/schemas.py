from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    external_product_id: str
    account_id: UUID | None = None
    title: str
    category: str | None = None
    price: float = 0
    delivery_mode: str = "auto"
    status: str = "active"
    auto_delivery_enabled: bool = True
    metadata_json: dict = {}


class ProductUpdate(BaseModel):
    title: str | None = None
    category: str | None = None
    price: float | None = None
    delivery_mode: str | None = None
    status: str | None = None
    auto_delivery_enabled: bool | None = None
    delivery_template_id: UUID | None = None
    faq_template_id: UUID | None = None
    rule_profile_id: UUID | None = None
    metadata_json: dict | None = None


class ProductRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    external_product_id: str
    account_id: UUID | None = None
    title: str
    category: str | None = None
    price: float
    delivery_mode: str
    delivery_template_id: UUID | None = None
    faq_template_id: UUID | None = None
    rule_profile_id: UUID | None = None
    auto_delivery_enabled: bool
    status: str
    metadata_json: dict
    updated_at: datetime

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class NotificationConfigCreate(BaseModel):
    channel: str
    name: str
    target: str | None = None
    config_json: dict = {}
    enabled: bool = True


class NotificationConfigUpdate(BaseModel):
    name: str | None = None
    target: str | None = None
    config_json: dict | None = None
    enabled: bool | None = None


class NotificationTestPayload(BaseModel):
    event_type: str = "manual_test"
    message: str = "FishFlow notification test"
    severity: str = "info"


class NotificationConfigRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    channel: str
    name: str
    target: str | None = None
    config_json: dict
    enabled: bool
    updated_at: datetime

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AppSettingCreate(BaseModel):
    key: str
    value_json: dict = {}


class AppSettingUpdate(BaseModel):
    value_json: dict


class AppSettingRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    key: str
    value_json: dict
    updated_at: datetime

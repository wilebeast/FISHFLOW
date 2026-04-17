from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AccountCreate(BaseModel):
    nickname: str
    external_account_id: str
    platform: str = "xianyu"
    login_status: str = "active"
    health_status: str = "healthy"
    credential_ref: str | None = None
    risk_level: str = "low"


class AccountUpdate(BaseModel):
    nickname: str | None = None
    login_status: str | None = None
    health_status: str | None = None
    credential_ref: str | None = None
    risk_level: str | None = None
    disabled_reason: str | None = None


class DisableAccountPayload(BaseModel):
    reason: str = "disabled by operator"


class AccountRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    platform: str
    nickname: str
    external_account_id: str
    login_status: str
    health_status: str
    credential_ref: str | None = None
    last_login_at: datetime | None = None
    last_check_at: datetime | None = None
    risk_level: str
    disabled_reason: str | None = None
    updated_at: datetime

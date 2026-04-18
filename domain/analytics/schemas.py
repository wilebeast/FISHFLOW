from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AnalyticsSnapshotRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    snapshot_date: date
    message_count: int
    auto_reply_count: int
    handoff_count: int
    delivery_success_count: int
    delivery_fail_count: int
    created_at: datetime


class AnalyticsOverview(BaseModel):
    snapshot_date: date | None = None
    message_count: int = 0
    auto_reply_count: int = 0
    handoff_count: int = 0
    delivery_success_count: int = 0
    delivery_fail_count: int = 0

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ConversationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    external_conversation_id: str
    account_id: UUID | None = None
    product_id: UUID | None = None
    buyer_id: str | None = None
    current_stage: str
    handoff_status: str
    last_message_at: datetime | None = None
    assigned_to: str | None = None
    priority: str
    unread_count: int
    summary: str | None = None
    tags: dict
    updated_at: datetime


class ConversationTagUpdate(BaseModel):
    tags: list[str]


class ConversationSendMessage(BaseModel):
    content: str

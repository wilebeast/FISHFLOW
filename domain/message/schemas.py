from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from domain.message.enums import ContentType, MessageDirection, ProcessedStatus, SenderType


class MessageCreate(BaseModel):
    conversation_id: UUID
    external_message_id: str | None = None
    sender_type: SenderType = SenderType.BUYER
    content_type: ContentType = ContentType.TEXT
    content: str
    direction: MessageDirection = MessageDirection.INBOUND


class MessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    conversation_id: UUID
    external_message_id: str | None = None
    sender_type: SenderType
    content_type: ContentType
    content: str
    normalized_content: str
    direction: MessageDirection
    processed_status: ProcessedStatus
    created_at: datetime

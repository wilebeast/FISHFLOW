from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.message.enums import ContentType, MessageDirection, ProcessedStatus, SenderType
from infrastructure.db.base import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    conversation_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("conversations.id"), index=True)
    external_message_id: Mapped[str | None] = mapped_column(String(128), unique=True, nullable=True, index=True)
    sender_type: Mapped[str] = mapped_column(String(16), default=SenderType.BUYER.value)
    content_type: Mapped[str] = mapped_column(String(16), default=ContentType.TEXT.value)
    content: Mapped[str] = mapped_column(Text)
    normalized_content: Mapped[str] = mapped_column(Text)
    direction: Mapped[str] = mapped_column(String(16), default=MessageDirection.INBOUND.value)
    processed_status: Mapped[str] = mapped_column(
        String(32), default=ProcessedStatus.PENDING.value, index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    inserted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    conversation: Mapped["Conversation"] = relationship(back_populates="messages")

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db.base import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    account_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("accounts.id"), nullable=True
    )
    product_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("products.id"), nullable=True
    )
    external_conversation_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    buyer_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    current_stage: Mapped[str] = mapped_column(String(32), default="new_inquiry")
    handoff_status: Mapped[str] = mapped_column(String(32), default="bot")
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    account: Mapped["Account | None"] = relationship(back_populates="conversations")
    product: Mapped["Product | None"] = relationship(back_populates="conversations")
    orders: Mapped[list["Order"]] = relationship(back_populates="conversation")
    messages: Mapped[list["Message"]] = relationship(back_populates="conversation")

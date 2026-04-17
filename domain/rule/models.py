from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Integer, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from domain.rule.enums import ActionType, RuleScope, TriggerType
from infrastructure.db.base import Base


class Rule(Base):
    __tablename__ = "rules"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(128))
    scope: Mapped[str] = mapped_column(String(32), default=RuleScope.GLOBAL.value, index=True)
    account_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True, index=True)
    product_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True, index=True)
    trigger_type: Mapped[str] = mapped_column(String(32), default=TriggerType.MESSAGE_RECEIVED.value)
    priority: Mapped[int] = mapped_column(Integer, default=100, index=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    conditions: Mapped[dict] = mapped_column(JSON, default=dict)
    action_type: Mapped[str] = mapped_column(String(32), default=ActionType.REPLY_TEXT.value)
    action_payload: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

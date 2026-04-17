from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Integer, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from domain.template.enums import TemplateOwnerType, TemplateType
from infrastructure.db.base import Base


class Template(Base):
    __tablename__ = "templates"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    template_type: Mapped[str] = mapped_column(String(32), default=TemplateType.REPLY.value, index=True)
    name: Mapped[str] = mapped_column(String(128))
    owner_type: Mapped[str] = mapped_column(
        String(32), default=TemplateOwnerType.SYSTEM.value, index=True
    )
    owner_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, nullable=True)
    content: Mapped[str] = mapped_column(Text)
    variables: Mapped[dict] = mapped_column(JSON, default=dict)
    version: Mapped[int] = mapped_column(Integer, default=1)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

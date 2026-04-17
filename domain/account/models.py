from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db.base import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    platform: Mapped[str] = mapped_column(String(32), default="xianyu")
    nickname: Mapped[str] = mapped_column(String(128))
    external_account_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    login_status: Mapped[str] = mapped_column(String(32), default="active")
    health_status: Mapped[str] = mapped_column(String(32), default="healthy")
    credential_ref: Mapped[str | None] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    orders: Mapped[list["Order"]] = relationship(back_populates="account")
    delivery_tasks: Mapped[list["DeliveryTask"]] = relationship(back_populates="account")
    products: Mapped[list["Product"]] = relationship(back_populates="account")
    conversations: Mapped[list["Conversation"]] = relationship(back_populates="account")

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.delivery.enums import DeliveryTaskStatus, DeliveryType
from infrastructure.db.base import Base


class DeliveryTask(Base):
    __tablename__ = "delivery_tasks"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    order_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("orders.id"), index=True
    )
    product_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("products.id"), nullable=True
    )
    account_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("accounts.id"), nullable=True
    )
    delivery_type: Mapped[str] = mapped_column(String(32), default=DeliveryType.SEND_TEXT.value)
    template_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("templates.id"), nullable=True)
    payload_snapshot: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(
        String(32), default=DeliveryTaskStatus.PENDING.value, index=True
    )
    attempt_count: Mapped[int] = mapped_column(Integer, default=0)
    max_attempts: Mapped[int] = mapped_column(Integer, default=3)
    idempotency_key: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    result_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    next_retry_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    executed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    order: Mapped["Order"] = relationship(back_populates="delivery_tasks")
    product: Mapped["Product | None"] = relationship(back_populates="delivery_tasks")
    account: Mapped["Account | None"] = relationship(back_populates="delivery_tasks")
    template: Mapped["Template | None"] = relationship()

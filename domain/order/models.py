from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Numeric, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.order.enums import DeliveryStatus, OrderStatus, PayStatus
from infrastructure.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    account_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("accounts.id"), nullable=True
    )
    product_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("products.id"), nullable=True
    )
    conversation_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("conversations.id"), nullable=True
    )
    external_order_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    buyer_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    currency: Mapped[str] = mapped_column(String(8), default="CNY")
    order_status: Mapped[str] = mapped_column(String(32), default=OrderStatus.CREATED.value, index=True)
    pay_status: Mapped[str] = mapped_column(String(32), default=PayStatus.UNPAID.value, index=True)
    delivery_status: Mapped[str] = mapped_column(
        String(32), default=DeliveryStatus.PENDING.value, index=True
    )
    paid_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    delivered_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    metadata_json: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    delivery_tasks: Mapped[list["DeliveryTask"]] = relationship(back_populates="order")
    product: Mapped["Product | None"] = relationship(back_populates="orders")
    conversation: Mapped["Conversation | None"] = relationship(back_populates="orders")
    account: Mapped["Account | None"] = relationship(back_populates="orders")

    @property
    def order_status_enum(self) -> OrderStatus:
        return OrderStatus(self.order_status)

    @property
    def pay_status_enum(self) -> PayStatus:
        return PayStatus(self.pay_status)

    @property
    def delivery_status_enum(self) -> DeliveryStatus:
        return DeliveryStatus(self.delivery_status)

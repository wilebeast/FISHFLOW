from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Numeric, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    account_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("accounts.id"), nullable=True
    )
    external_product_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    category: Mapped[str | None] = mapped_column(String(64), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    delivery_mode: Mapped[str] = mapped_column(String(32), default="auto")
    status: Mapped[str] = mapped_column(String(32), default="active")
    metadata_json: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    account: Mapped["Account | None"] = relationship(back_populates="products")
    orders: Mapped[list["Order"]] = relationship(back_populates="product")
    delivery_tasks: Mapped[list["DeliveryTask"]] = relationship(back_populates="product")
    conversations: Mapped[list["Conversation"]] = relationship(back_populates="product")

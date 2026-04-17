from __future__ import annotations

from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from domain.order.models import Order


class OrderRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _coerce_uuid(order_id: UUID | str) -> UUID:
        return order_id if isinstance(order_id, UUID) else UUID(str(order_id))

    def get_by_external_order_id(self, external_order_id: str) -> Order | None:
        stmt = select(Order).where(Order.external_order_id == external_order_id)
        return self.session.scalar(stmt)

    def get(self, order_id: UUID | str) -> Order | None:
        stmt = select(Order).where(Order.id == self._coerce_uuid(order_id))
        return self.session.scalar(stmt)

    def list_recent(self, limit: int = 50, offset: int = 0) -> list[Order]:
        stmt = select(Order).order_by(desc(Order.created_at)).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

    def save(self, order: Order) -> Order:
        self.session.add(order)
        self.session.flush()
        return order

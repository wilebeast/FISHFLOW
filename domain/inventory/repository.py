from __future__ import annotations

from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from domain.inventory.models import InventoryItem


class InventoryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _coerce_uuid(value: UUID | str) -> UUID:
        return value if isinstance(value, UUID) else UUID(str(value))

    def get(self, item_id: UUID | str) -> InventoryItem | None:
        stmt = select(InventoryItem).where(InventoryItem.id == self._coerce_uuid(item_id))
        return self.session.scalar(stmt)

    def list_recent(
        self,
        resource_type: str | None = None,
        status: str | None = None,
        product_id: UUID | str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[InventoryItem]:
        stmt = select(InventoryItem)
        if resource_type:
            stmt = stmt.where(InventoryItem.resource_type == resource_type)
        if status:
            stmt = stmt.where(InventoryItem.status == status)
        if product_id:
            stmt = stmt.where(InventoryItem.product_id == self._coerce_uuid(product_id))
        stmt = stmt.order_by(desc(InventoryItem.updated_at)).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

    def save(self, item: InventoryItem) -> InventoryItem:
        self.session.add(item)
        self.session.flush()
        return item

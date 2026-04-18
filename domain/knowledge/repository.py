from __future__ import annotations

from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from domain.knowledge.models import KnowledgeItem


class KnowledgeRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _coerce_uuid(value: UUID | str) -> UUID:
        return value if isinstance(value, UUID) else UUID(str(value))

    def get(self, item_id: UUID | str) -> KnowledgeItem | None:
        stmt = select(KnowledgeItem).where(KnowledgeItem.id == self._coerce_uuid(item_id))
        return self.session.scalar(stmt)

    def list_recent(
        self,
        category: str | None = None,
        enabled: bool | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[KnowledgeItem]:
        stmt = select(KnowledgeItem)
        if category:
            stmt = stmt.where(KnowledgeItem.category == category)
        if enabled is not None:
            stmt = stmt.where(KnowledgeItem.enabled == enabled)
        stmt = stmt.order_by(desc(KnowledgeItem.updated_at)).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

    def save(self, item: KnowledgeItem) -> KnowledgeItem:
        self.session.add(item)
        self.session.flush()
        return item

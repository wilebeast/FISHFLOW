from __future__ import annotations

from domain.knowledge.models import KnowledgeItem
from domain.knowledge.schemas import KnowledgeUpdate


class KnowledgeService:
    @staticmethod
    def apply_update(item: KnowledgeItem, payload: KnowledgeUpdate) -> KnowledgeItem:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(item, field, value)
        return item

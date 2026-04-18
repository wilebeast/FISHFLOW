from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from domain.ai_copy.models import AICopyHistory


class AICopyHistoryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_recent(self, scene: str | None = None, limit: int = 50) -> list[AICopyHistory]:
        stmt = select(AICopyHistory)
        if scene:
            stmt = stmt.where(AICopyHistory.scene == scene)
        stmt = stmt.order_by(desc(AICopyHistory.created_at)).limit(limit)
        return list(self.session.scalars(stmt).all())

    def save(self, item: AICopyHistory) -> AICopyHistory:
        self.session.add(item)
        self.session.flush()
        return item

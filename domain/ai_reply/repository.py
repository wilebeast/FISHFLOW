from __future__ import annotations

from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from domain.ai_reply.models import AICallLog, AIReplyConfig


class AIReplyConfigRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _coerce_uuid(value: UUID | str) -> UUID:
        return value if isinstance(value, UUID) else UUID(str(value))

    def get(self, config_id: UUID | str) -> AIReplyConfig | None:
        stmt = select(AIReplyConfig).where(AIReplyConfig.id == self._coerce_uuid(config_id))
        return self.session.scalar(stmt)

    def get_default(self) -> AIReplyConfig | None:
        stmt = select(AIReplyConfig).order_by(desc(AIReplyConfig.updated_at)).limit(1)
        return self.session.scalar(stmt)

    def save(self, config: AIReplyConfig) -> AIReplyConfig:
        self.session.add(config)
        self.session.flush()
        return config


class AICallLogRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_recent(self, limit: int = 50) -> list[AICallLog]:
        stmt = select(AICallLog).order_by(desc(AICallLog.created_at)).limit(limit)
        return list(self.session.scalars(stmt).all())

    def save(self, log: AICallLog) -> AICallLog:
        self.session.add(log)
        self.session.flush()
        return log

from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from domain.system_event.models import SystemEvent


class SystemEventRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_recent(self, limit: int = 50) -> list[SystemEvent]:
        stmt = select(SystemEvent).order_by(desc(SystemEvent.created_at)).limit(limit)
        return list(self.session.scalars(stmt).all())

    def save(self, event: SystemEvent) -> SystemEvent:
        self.session.add(event)
        self.session.flush()
        return event

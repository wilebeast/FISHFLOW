from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from domain.admin_action.models import AdminAction


class AdminActionRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, action: AdminAction) -> AdminAction:
        self.session.add(action)
        self.session.flush()
        return action

    def list_recent(self, limit: int = 50) -> list[AdminAction]:
        stmt = select(AdminAction).order_by(desc(AdminAction.created_at)).limit(limit)
        return list(self.session.scalars(stmt).all())

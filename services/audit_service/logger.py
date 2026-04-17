from __future__ import annotations

from sqlalchemy.orm import Session

from domain.admin_action.models import AdminAction
from domain.admin_action.repository import AdminActionRepository


class AuditLogger:
    def __init__(self, session: Session) -> None:
        self.repository = AdminActionRepository(session)

    def log(self, action: str, target_type: str, target_id: str, payload: dict, actor: str = "system") -> None:
        self.repository.save(
            AdminAction(
                actor=actor,
                action=action,
                target_type=target_type,
                target_id=target_id,
                payload=payload,
            )
        )

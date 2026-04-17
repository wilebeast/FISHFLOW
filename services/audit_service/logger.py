from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date, datetime
from uuid import UUID

from sqlalchemy.orm import Session

from domain.admin_action.models import AdminAction
from domain.admin_action.repository import AdminActionRepository


def _to_jsonable(value):
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {str(key): _to_jsonable(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_to_jsonable(item) for item in value]
    return value


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
                payload=_to_jsonable(payload),
            )
        )

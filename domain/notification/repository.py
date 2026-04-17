from __future__ import annotations

from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from domain.notification.models import NotificationConfig


class NotificationConfigRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _coerce_uuid(value: UUID | str) -> UUID:
        return value if isinstance(value, UUID) else UUID(str(value))

    def get(self, config_id: UUID | str) -> NotificationConfig | None:
        stmt = select(NotificationConfig).where(NotificationConfig.id == self._coerce_uuid(config_id))
        return self.session.scalar(stmt)

    def list_recent(self, channel: str | None = None, enabled: bool | None = None) -> list[NotificationConfig]:
        stmt = select(NotificationConfig)
        if channel:
            stmt = stmt.where(NotificationConfig.channel == channel)
        if enabled is not None:
            stmt = stmt.where(NotificationConfig.enabled == enabled)
        stmt = stmt.order_by(desc(NotificationConfig.updated_at))
        return list(self.session.scalars(stmt).all())

    def save(self, config: NotificationConfig) -> NotificationConfig:
        self.session.add(config)
        self.session.flush()
        return config

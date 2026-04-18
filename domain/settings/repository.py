from __future__ import annotations

from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from domain.settings.models import AppSetting


class AppSettingRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _coerce_uuid(value: UUID | str) -> UUID:
        return value if isinstance(value, UUID) else UUID(str(value))

    def get(self, item_id: UUID | str) -> AppSetting | None:
        stmt = select(AppSetting).where(AppSetting.id == self._coerce_uuid(item_id))
        return self.session.scalar(stmt)

    def get_by_key(self, key: str) -> AppSetting | None:
        stmt = select(AppSetting).where(AppSetting.key == key)
        return self.session.scalar(stmt)

    def list_recent(self, limit: int = 50) -> list[AppSetting]:
        stmt = select(AppSetting).order_by(desc(AppSetting.updated_at)).limit(limit)
        return list(self.session.scalars(stmt).all())

    def save(self, item: AppSetting) -> AppSetting:
        self.session.add(item)
        self.session.flush()
        return item

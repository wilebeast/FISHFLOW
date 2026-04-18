from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from domain.analytics.models import AnalyticsSnapshot


class AnalyticsRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_recent(self, limit: int = 30) -> list[AnalyticsSnapshot]:
        stmt = select(AnalyticsSnapshot).order_by(desc(AnalyticsSnapshot.snapshot_date)).limit(limit)
        return list(self.session.scalars(stmt).all())

    def get_latest(self) -> AnalyticsSnapshot | None:
        stmt = select(AnalyticsSnapshot).order_by(desc(AnalyticsSnapshot.snapshot_date)).limit(1)
        return self.session.scalar(stmt)

    def save(self, snapshot: AnalyticsSnapshot) -> AnalyticsSnapshot:
        self.session.add(snapshot)
        self.session.flush()
        return snapshot

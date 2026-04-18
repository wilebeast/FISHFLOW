from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from domain.analytics.repository import AnalyticsRepository
from domain.analytics.schemas import AnalyticsOverview, AnalyticsSnapshotRead
from infrastructure.db.session import get_db


router = APIRouter()


@router.get("/overview", response_model=AnalyticsOverview)
def analytics_overview(db: Session = Depends(get_db)) -> AnalyticsOverview:
    latest = AnalyticsRepository(db).get_latest()
    if latest is None:
        return AnalyticsOverview()
    return AnalyticsOverview(
        snapshot_date=latest.snapshot_date,
        message_count=latest.message_count,
        auto_reply_count=latest.auto_reply_count,
        handoff_count=latest.handoff_count,
        delivery_success_count=latest.delivery_success_count,
        delivery_fail_count=latest.delivery_fail_count,
    )


@router.get("/history", response_model=list[AnalyticsSnapshotRead])
def analytics_history(db: Session = Depends(get_db)) -> list[AnalyticsSnapshotRead]:
    return AnalyticsRepository(db).list_recent()

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from domain.system_event.schemas import SystemEventRead
from infrastructure.config.settings import get_settings
from infrastructure.db.session import get_db
from services.system_service.health import SystemHealthService


router = APIRouter()


@router.get("/health")
def system_health(db: Session = Depends(get_db)) -> dict:
    settings = get_settings()
    return SystemHealthService(db, settings.redis_url).get_health()


@router.get("/queue")
def queue_health(db: Session = Depends(get_db)) -> dict:
    settings = get_settings()
    return SystemHealthService(db, settings.redis_url).get_queue()


@router.get("/errors", response_model=list[SystemEventRead])
def system_errors(db: Session = Depends(get_db)) -> list[SystemEventRead]:
    settings = get_settings()
    return SystemHealthService(db, settings.redis_url).get_recent_errors()

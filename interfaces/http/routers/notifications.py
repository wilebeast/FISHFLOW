from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from domain.notification.models import NotificationConfig
from domain.notification.repository import NotificationConfigRepository
from domain.notification.schemas import (
    NotificationConfigCreate,
    NotificationConfigRead,
    NotificationConfigUpdate,
    NotificationTestPayload,
)
from domain.notification.service import NotificationConfigService
from domain.system_event.models import SystemEvent
from domain.system_event.repository import SystemEventRepository
from infrastructure.db.session import get_db
from interfaces.http.routers.dto.common import ActionAccepted
from services.audit_service.logger import AuditLogger


router = APIRouter()


@router.get("/config", response_model=list[NotificationConfigRead])
def list_notification_configs(
    channel: str | None = Query(default=None),
    enabled: bool | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[NotificationConfig]:
    return NotificationConfigRepository(db).list_recent(channel=channel, enabled=enabled)


@router.post("/config", response_model=NotificationConfigRead)
def create_notification_config(payload: NotificationConfigCreate, db: Session = Depends(get_db)) -> NotificationConfig:
    config = NotificationConfig(**payload.model_dump())
    NotificationConfigRepository(db).save(config)
    AuditLogger(db).log("create_notification_config", "notification", str(config.id), payload.model_dump())
    db.commit()
    db.refresh(config)
    return config


@router.patch("/config/{config_id}", response_model=NotificationConfigRead)
def update_notification_config(
    config_id: str, payload: NotificationConfigUpdate, db: Session = Depends(get_db)
) -> NotificationConfig:
    repository = NotificationConfigRepository(db)
    config = repository.get(config_id)
    if config is None:
        raise HTTPException(status_code=404, detail="notification config not found")
    NotificationConfigService.apply_update(config, payload)
    AuditLogger(db).log(
        "update_notification_config",
        "notification",
        str(config.id),
        payload.model_dump(exclude_unset=True),
    )
    db.commit()
    db.refresh(config)
    return config


@router.post("/test", response_model=ActionAccepted)
def test_notification(payload: NotificationTestPayload, db: Session = Depends(get_db)) -> ActionAccepted:
    SystemEventRepository(db).save(
        SystemEvent(
            event_type=payload.event_type,
            severity=payload.severity,
            source="notification_test",
            message=payload.message,
            details={"message": payload.message},
        )
    )
    AuditLogger(db).log("test_notification", "notification", "system", payload.model_dump())
    db.commit()
    return ActionAccepted(status="ok", detail="notification test recorded")

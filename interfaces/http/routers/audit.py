from __future__ import annotations

from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session

from domain.admin_action.repository import AdminActionRepository
from domain.system_event.repository import SystemEventRepository
from domain.system_event.schemas import SystemEventRead
from infrastructure.db.session import get_db


router = APIRouter()


class AdminActionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    actor: str
    action: str
    target_type: str
    target_id: str
    payload: dict
    created_at: datetime


@router.get("/admin-actions", response_model=list[AdminActionRead])
def list_admin_actions(
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> list[AdminActionRead]:
    return AdminActionRepository(db).list_recent(limit=limit)


@router.get("/system-events", response_model=list[SystemEventRead])
def list_system_events(
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> list[SystemEventRead]:
    return SystemEventRepository(db).list_recent(limit=limit)

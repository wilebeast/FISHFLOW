from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from domain.settings.models import AppSetting
from domain.settings.repository import AppSettingRepository
from domain.settings.schemas import AppSettingCreate, AppSettingRead, AppSettingUpdate
from infrastructure.db.session import get_db
from interfaces.http.routers.dto.common import ActionAccepted
from services.audit_service.logger import AuditLogger


router = APIRouter()


@router.get("", response_model=list[AppSettingRead])
def list_settings(db: Session = Depends(get_db)) -> list[AppSettingRead]:
    return AppSettingRepository(db).list_recent()


@router.post("", response_model=AppSettingRead)
def create_setting(payload: AppSettingCreate, db: Session = Depends(get_db)) -> AppSetting:
    existing = AppSettingRepository(db).get_by_key(payload.key)
    if existing:
        existing.value_json = payload.value_json
        AuditLogger(db).log("update_setting", "setting", str(existing.id), payload.model_dump())
        db.commit()
        db.refresh(existing)
        return existing
    item = AppSetting(**payload.model_dump())
    AppSettingRepository(db).save(item)
    AuditLogger(db).log("create_setting", "setting", str(item.id), payload.model_dump())
    db.commit()
    db.refresh(item)
    return item


@router.patch("/{item_id}", response_model=AppSettingRead)
def update_setting(item_id: str, payload: AppSettingUpdate, db: Session = Depends(get_db)) -> AppSetting:
    repository = AppSettingRepository(db)
    item = repository.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="setting not found")
    item.value_json = payload.value_json
    AuditLogger(db).log("update_setting", "setting", str(item.id), payload.model_dump())
    db.commit()
    db.refresh(item)
    return item


@router.post("/export", response_model=dict)
def export_settings(db: Session = Depends(get_db)) -> dict:
    settings = AppSettingRepository(db).list_recent(limit=200)
    return {item.key: item.value_json for item in settings}


@router.post("/import", response_model=ActionAccepted)
def import_settings(payload: dict, db: Session = Depends(get_db)) -> ActionAccepted:
    repository = AppSettingRepository(db)
    for key, value in payload.items():
        item = repository.get_by_key(key)
        if item is None:
            repository.save(AppSetting(key=key, value_json=value))
        else:
            item.value_json = value
    AuditLogger(db).log("import_settings", "setting", "bulk", {"keys": list(payload.keys())})
    db.commit()
    return ActionAccepted(status="ok", detail="settings imported")

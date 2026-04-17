from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from domain.ai_reply.models import AIReplyConfig
from domain.ai_reply.repository import AICallLogRepository, AIReplyConfigRepository
from domain.ai_reply.schemas import (
    AICallLogRead,
    AIReplyConfigCreate,
    AIReplyConfigRead,
    AIReplyConfigUpdate,
    AIReplyTestPayload,
)
from domain.ai_reply.service import AIReplyConfigService, AIReplyService
from infrastructure.db.session import get_db
from services.audit_service.logger import AuditLogger


router = APIRouter()


class AIReplyTestResult(BaseModel):
    reply: str


@router.get("/config", response_model=AIReplyConfigRead | None)
def get_ai_reply_config(db: Session = Depends(get_db)) -> AIReplyConfig | None:
    return AIReplyConfigRepository(db).get_default()


@router.post("/config", response_model=AIReplyConfigRead)
def create_ai_reply_config(payload: AIReplyConfigCreate, db: Session = Depends(get_db)) -> AIReplyConfig:
    config = AIReplyConfig(**payload.model_dump())
    AIReplyConfigRepository(db).save(config)
    AuditLogger(db).log("create_ai_reply_config", "ai_reply", str(config.id), payload.model_dump())
    db.commit()
    db.refresh(config)
    return config


@router.patch("/config/{config_id}", response_model=AIReplyConfigRead)
def update_ai_reply_config(config_id: str, payload: AIReplyConfigUpdate, db: Session = Depends(get_db)) -> AIReplyConfig:
    repository = AIReplyConfigRepository(db)
    config = repository.get(config_id)
    if config is None:
        raise HTTPException(status_code=404, detail="ai reply config not found")
    AIReplyConfigService.apply_update(config, payload)
    AuditLogger(db).log("update_ai_reply_config", "ai_reply", str(config.id), payload.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(config)
    return config


@router.post("/test", response_model=AIReplyTestResult)
def test_ai_reply(payload: AIReplyTestPayload, db: Session = Depends(get_db)) -> AIReplyTestResult:
    config = AIReplyConfigRepository(db).get_default()
    if config is None:
        raise HTTPException(status_code=400, detail="ai reply config not initialized")
    reply = AIReplyService(AICallLogRepository(db)).generate_demo_reply(config, payload)
    AuditLogger(db).log("test_ai_reply", "ai_reply", str(config.id), payload.model_dump())
    db.commit()
    return AIReplyTestResult(**reply)


@router.get("/logs", response_model=list[AICallLogRead])
def list_ai_reply_logs(db: Session = Depends(get_db)) -> list[AICallLogRead]:
    return AICallLogRepository(db).list_recent()

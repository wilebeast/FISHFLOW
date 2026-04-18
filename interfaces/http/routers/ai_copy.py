from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from domain.ai_copy.repository import AICopyHistoryRepository
from domain.ai_copy.schemas import AICopyGeneratePayload, AICopyHistoryRead, AICopyResult
from domain.ai_copy.service import AICopyService
from infrastructure.db.session import get_db
from services.audit_service.logger import AuditLogger


router = APIRouter()


@router.post("/generate", response_model=AICopyResult)
def generate_copy(payload: AICopyGeneratePayload, db: Session = Depends(get_db)) -> AICopyResult:
    result = AICopyService(AICopyHistoryRepository(db)).generate(payload)
    AuditLogger(db).log("generate_ai_copy", "ai_copy", payload.scene, payload.model_dump())
    db.commit()
    return AICopyResult(**result)


@router.get("/history", response_model=list[AICopyHistoryRead])
def list_copy_history(
    scene: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> list[AICopyHistoryRead]:
    return AICopyHistoryRepository(db).list_recent(scene=scene, limit=limit)

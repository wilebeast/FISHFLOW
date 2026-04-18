from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from domain.knowledge.models import KnowledgeItem
from domain.knowledge.repository import KnowledgeRepository
from domain.knowledge.schemas import KnowledgeCreate, KnowledgeRead, KnowledgeUpdate
from domain.knowledge.service import KnowledgeService
from infrastructure.db.session import get_db
from services.audit_service.logger import AuditLogger


router = APIRouter()


@router.get("", response_model=list[KnowledgeRead])
def list_knowledge(
    category: str | None = Query(default=None),
    enabled: bool | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[KnowledgeRead]:
    return KnowledgeRepository(db).list_recent(category=category, enabled=enabled, limit=limit, offset=offset)


@router.post("", response_model=KnowledgeRead)
def create_knowledge(payload: KnowledgeCreate, db: Session = Depends(get_db)) -> KnowledgeItem:
    item = KnowledgeItem(**payload.model_dump())
    KnowledgeRepository(db).save(item)
    AuditLogger(db).log("create_knowledge", "knowledge", str(item.id), payload.model_dump())
    db.commit()
    db.refresh(item)
    return item


@router.get("/{item_id}", response_model=KnowledgeRead)
def get_knowledge(item_id: str, db: Session = Depends(get_db)) -> KnowledgeItem:
    item = KnowledgeRepository(db).get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="knowledge item not found")
    return item


@router.patch("/{item_id}", response_model=KnowledgeRead)
def update_knowledge(item_id: str, payload: KnowledgeUpdate, db: Session = Depends(get_db)) -> KnowledgeItem:
    repository = KnowledgeRepository(db)
    item = repository.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="knowledge item not found")
    KnowledgeService.apply_update(item, payload)
    AuditLogger(db).log("update_knowledge", "knowledge", str(item.id), payload.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(item)
    return item

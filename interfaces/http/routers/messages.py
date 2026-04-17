from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from domain.message.repository import MessageRepository
from domain.message.schemas import MessageRead
from infrastructure.db.session import get_db


router = APIRouter()


@router.get("", response_model=list[MessageRead])
def list_messages(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[MessageRead]:
    repository = MessageRepository(db)
    return repository.list_recent(limit=limit, offset=offset)

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from domain.message.repository import MessageRepository
from domain.message.schemas import MessageRead
from infrastructure.db.session import get_db
from interfaces.http.routers.dto.common import ActionAccepted
from services.message_service.sender import MessageSender


router = APIRouter()


class MessageSendPayload(BaseModel):
    content: str
    reply_to_message_id: str | None = None


@router.get("", response_model=list[MessageRead])
def list_messages(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[MessageRead]:
    repository = MessageRepository(db)
    return repository.list_recent(limit=limit, offset=offset)


@router.get("/{message_id}", response_model=MessageRead)
def get_message(message_id: str, db: Session = Depends(get_db)) -> MessageRead:
    message = MessageRepository(db).get(message_id)
    if message is None:
        raise HTTPException(status_code=404, detail="message not found")
    return message


@router.post("/{conversation_id}/send", response_model=ActionAccepted)
def send_message(conversation_id: str, payload: MessageSendPayload, db: Session = Depends(get_db)) -> ActionAccepted:
    message = MessageSender(db).send_manual(conversation_id, payload.content, payload.reply_to_message_id)
    db.commit()
    return ActionAccepted(status="ok", detail=f"message sent {message.id}")

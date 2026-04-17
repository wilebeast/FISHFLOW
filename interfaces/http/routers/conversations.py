from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from domain.conversation.repository import ConversationRepository
from domain.conversation.schemas import ConversationRead, ConversationSendMessage, ConversationTagUpdate
from domain.conversation.service import ConversationService
from domain.message.repository import MessageRepository
from domain.message.schemas import MessageRead
from infrastructure.db.session import get_db
from interfaces.http.routers.dto.common import ActionAccepted
from services.audit_service.logger import AuditLogger
from services.message_service.sender import MessageSender


router = APIRouter()


@router.get("", response_model=list[ConversationRead])
def list_conversations(
    product_id: str | None = Query(default=None),
    handoff_status: str | None = Query(default=None),
    buyer_id: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[ConversationRead]:
    return ConversationRepository(db).list_recent(
        product_id=product_id,
        handoff_status=handoff_status,
        buyer_id=buyer_id,
        limit=limit,
        offset=offset,
    )


@router.get("/{conversation_id}", response_model=ConversationRead)
def get_conversation(conversation_id: str, db: Session = Depends(get_db)) -> ConversationRead:
    conversation = ConversationRepository(db).get(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="conversation not found")
    return conversation


@router.get("/{conversation_id}/messages", response_model=list[MessageRead])
def get_conversation_messages(conversation_id: str, db: Session = Depends(get_db)) -> list[MessageRead]:
    conversation = ConversationRepository(db).get(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="conversation not found")
    return MessageRepository(db).list_by_conversation(conversation.id)


@router.post("/{conversation_id}/handoff", response_model=ActionAccepted)
def handoff_conversation(conversation_id: str, db: Session = Depends(get_db)) -> ActionAccepted:
    repository = ConversationRepository(db)
    conversation = repository.get(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="conversation not found")
    ConversationService().handoff(conversation)
    AuditLogger(db).log("handoff_conversation", "conversation", str(conversation.id), {})
    db.commit()
    return ActionAccepted(status="ok", detail="conversation handed off")


@router.post("/{conversation_id}/release", response_model=ActionAccepted)
def release_conversation(conversation_id: str, db: Session = Depends(get_db)) -> ActionAccepted:
    repository = ConversationRepository(db)
    conversation = repository.get(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="conversation not found")
    ConversationService().release(conversation)
    AuditLogger(db).log("release_conversation", "conversation", str(conversation.id), {})
    db.commit()
    return ActionAccepted(status="ok", detail="conversation released")


@router.post("/{conversation_id}/tags", response_model=ActionAccepted)
def update_conversation_tags(
    conversation_id: str,
    payload: ConversationTagUpdate,
    db: Session = Depends(get_db),
) -> ActionAccepted:
    repository = ConversationRepository(db)
    conversation = repository.get(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="conversation not found")
    ConversationService().set_tags(conversation, payload.tags)
    AuditLogger(db).log("update_conversation_tags", "conversation", str(conversation.id), payload.model_dump())
    db.commit()
    return ActionAccepted(status="ok", detail="tags updated")


@router.post("/{conversation_id}/send", response_model=MessageRead)
def send_message(
    conversation_id: str,
    payload: ConversationSendMessage,
    db: Session = Depends(get_db),
) -> MessageRead:
    conversation = ConversationRepository(db).get(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="conversation not found")
    message = MessageSender(db).send_manual(conversation_id, payload.content)
    AuditLogger(db).log("send_message", "conversation", str(conversation.id), payload.model_dump())
    db.commit()
    db.refresh(message)
    return message

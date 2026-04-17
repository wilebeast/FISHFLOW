from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.worker.tasks_message import process_inbound_message
from apps.worker.tasks_order import handle_paid_event
from domain.conversation.models import Conversation
from domain.message.enums import ContentType, MessageDirection, SenderType
from domain.message.schemas import MessageCreate
from infrastructure.db.session import get_db
from services.message_service.processor import MessageProcessor


router = APIRouter()


class MessageReceivedPayload(BaseModel):
    conversation_id: UUID | None = None
    external_conversation_id: str | None = None
    external_message_id: str | None = None
    sender_type: SenderType = SenderType.BUYER
    content_type: ContentType = ContentType.TEXT
    content: str


@router.post("/orders/paid")
def order_paid_event(order_id: str, background_tasks: BackgroundTasks) -> dict[str, str]:
    background_tasks.add_task(handle_paid_event.delay, order_id, True)
    return {"status": "accepted", "order_id": order_id}


@router.post("/messages/received")
def message_received_event(
    payload: MessageReceivedPayload,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    conversation_id = payload.conversation_id
    if conversation_id is None and payload.external_conversation_id:
        stmt = select(Conversation).where(
            Conversation.external_conversation_id == payload.external_conversation_id
        )
        conversation = db.scalar(stmt)
        if conversation is None:
            raise HTTPException(status_code=404, detail="conversation not found")
        conversation_id = conversation.id

    if conversation_id is None:
        raise HTTPException(status_code=400, detail="conversation_id is required")

    processor = MessageProcessor(db)
    message = processor.ingest_message(
        MessageCreate(
            conversation_id=conversation_id,
            external_message_id=payload.external_message_id,
            sender_type=payload.sender_type,
            content_type=payload.content_type,
            content=payload.content,
            direction=MessageDirection.INBOUND,
        )
    )
    db.commit()
    db.refresh(message)
    background_tasks.add_task(process_inbound_message.delay, str(message.id))

    return {"status": "accepted", "message_id": str(message.id), "conversation_id": str(message.conversation_id)}

from __future__ import annotations

from apps.worker.celery_app import celery_app
from infrastructure.db.session import SessionLocal
from services.message_service.processor import MessageProcessor
from services.message_service.sender import MessageSender


@celery_app.task(name="messages.process_inbound")
def process_inbound_message(message_id: str) -> str:
    session = SessionLocal()
    try:
        processor = MessageProcessor(session)
        message, reply_message, _route = processor.process_inbound_message(message_id)
        if reply_message is not None:
            MessageSender(session).send_existing(reply_message.id)
        session.commit()
        return str(reply_message.id if reply_message else message.id)
    finally:
        session.close()

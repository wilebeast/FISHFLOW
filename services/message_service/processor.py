from __future__ import annotations

from sqlalchemy.orm import Session

from domain.conversation.models import Conversation
from domain.message.enums import MessageDirection, ProcessedStatus, SenderType
from domain.message.models import Message
from domain.message.repository import MessageRepository
from domain.message.schemas import MessageCreate
from domain.message.service import MessageService
from domain.rule.enums import ActionType
from domain.rule.repository import RuleRepository
from services.message_service.router import MessageRouteResult, MessageRouter


class MessageProcessor:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.message_repository = MessageRepository(session)
        self.message_service = MessageService()
        self.rule_repository = RuleRepository(session)
        self.router = MessageRouter(self.rule_repository)

    def ingest_message(self, payload: MessageCreate) -> Message:
        if payload.external_message_id:
            existing = self.message_repository.get_by_external_message_id(payload.external_message_id)
            if existing:
                return existing

        message = Message(
            conversation_id=payload.conversation_id,
            external_message_id=payload.external_message_id,
            sender_type=payload.sender_type.value,
            content_type=payload.content_type.value,
            content=payload.content,
            normalized_content=self.message_service.normalize_content(payload.content),
            direction=payload.direction.value,
            processed_status=ProcessedStatus.PENDING.value,
        )
        self.message_repository.save(message)
        self.session.flush()
        return message

    def process_inbound_message(self, message_id: str) -> tuple[Message, Message | None, MessageRouteResult]:
        message = self.message_repository.get(message_id)
        if message is None:
            raise ValueError(f"message not found: {message_id}")

        context = {
            "event": "message_received",
            "normalized_content": message.normalized_content,
            "content": message.content,
        }
        route = self.router.route(context)
        reply_message = None

        if route.action_type in {ActionType.REPLY_TEXT.value, ActionType.REPLY_TEMPLATE.value}:
            reply_content = route.action_payload.get("content", "")
            reply_message = Message(
                conversation_id=message.conversation_id,
                sender_type=SenderType.BOT.value,
                content_type=message.content_type,
                content=reply_content,
                normalized_content=self.message_service.normalize_content(reply_content),
                direction=MessageDirection.OUTBOUND.value,
                processed_status=ProcessedStatus.PROCESSED.value,
            )
            self.message_repository.save(reply_message)
        elif route.action_type == ActionType.REPLY_AI.value:
            reply_content = "已收到消息，稍后为您处理。"
            reply_message = Message(
                conversation_id=message.conversation_id,
                sender_type=SenderType.BOT.value,
                content_type=message.content_type,
                content=reply_content,
                normalized_content=self.message_service.normalize_content(reply_content),
                direction=MessageDirection.OUTBOUND.value,
                processed_status=ProcessedStatus.PROCESSED.value,
            )
            self.message_repository.save(reply_message)

        self.message_service.mark_processed(message)

        conversation = self.session.get(Conversation, message.conversation_id)
        if conversation is not None:
            conversation.summary = message.content[:280]
            conversation.last_message_at = message.created_at
            conversation.unread_count = max(conversation.unread_count, 0) + 1

        self.session.flush()
        return message, reply_message, route

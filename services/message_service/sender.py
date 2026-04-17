from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from domain.conversation.repository import ConversationRepository
from domain.message.enums import ContentType, MessageDirection, ProcessedStatus, SenderType
from domain.message.models import Message
from domain.message.repository import MessageRepository
from domain.message.service import MessageService


class MessageSender:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.messages = MessageRepository(session)
        self.conversations = ConversationRepository(session)
        self.message_service = MessageService()

    def send_manual(
        self,
        conversation_id: str | UUID,
        content: str,
        reply_to_message_id: str | UUID | None = None,
    ) -> Message:
        normalized_conversation_id = (
            conversation_id if isinstance(conversation_id, UUID) else UUID(str(conversation_id))
        )
        normalized_reply_to_id = None
        if reply_to_message_id is not None:
            normalized_reply_to_id = (
                reply_to_message_id
                if isinstance(reply_to_message_id, UUID)
                else UUID(str(reply_to_message_id))
            )
        message = Message(
            conversation_id=normalized_conversation_id,
            reply_to_message_id=normalized_reply_to_id,
            sender_type=SenderType.SELLER.value,
            content_type=ContentType.TEXT.value,
            content=content,
            normalized_content=self.message_service.normalize_content(content),
            direction=MessageDirection.OUTBOUND.value,
            processed_status=ProcessedStatus.PROCESSED.value,
        )
        self.message_service.mark_sent(message)
        self.messages.save(message)
        conversation = self.conversations.get(normalized_conversation_id)
        if conversation is not None:
            conversation.last_message_at = message.created_at
            conversation.unread_count = 0
        self.session.flush()
        return message

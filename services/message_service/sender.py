from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from domain.account.models import Account
from domain.conversation.models import Conversation
from domain.conversation.repository import ConversationRepository
from domain.message.enums import ContentType, MessageDirection, ProcessedStatus, SenderType
from domain.message.models import Message
from domain.message.repository import MessageRepository
from domain.message.service import MessageService
from services.channel_adapter.xianyu.sync_service import XianyuSyncService


class MessageSender:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.messages = MessageRepository(session)
        self.conversations = ConversationRepository(session)
        self.message_service = MessageService()
        self.xianyu = XianyuSyncService(session)

    def _resolve_send_context(self, conversation_id: UUID) -> tuple[Account, Conversation]:
        conversation = self.conversations.get(conversation_id)
        if conversation is None:
            raise ValueError(f"conversation not found: {conversation_id}")
        if conversation.account is None:
            raise ValueError("conversation is not bound to an account")
        if not conversation.external_conversation_id:
            raise ValueError("conversation missing external_conversation_id")
        return conversation.account, conversation

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
        self.messages.save(message)
        conversation = self.conversations.get(normalized_conversation_id)
        if conversation is not None:
            conversation.last_message_at = message.created_at
            conversation.unread_count = 0
        self.message_service.mark_send_pending(message)
        try:
            account, resolved_conversation = self._resolve_send_context(normalized_conversation_id)
            response = self.xianyu.send_message(account, resolved_conversation, content)
            trace_id = str(response.get("trace_id") or response.get("message_id") or "")
            self.message_service.mark_sent(message)
            if trace_id:
                message.trace_id = trace_id
        except Exception as exc:
            self.message_service.mark_send_failed(message, str(exc))
        self.session.flush()
        return message

    def send_existing(self, message_id: str | UUID) -> Message:
        normalized_message_id = message_id if isinstance(message_id, UUID) else UUID(str(message_id))
        message = self.messages.get(normalized_message_id)
        if message is None:
            raise ValueError(f"message not found: {message_id}")
        account, conversation = self._resolve_send_context(message.conversation_id)
        self.message_service.mark_send_pending(message)
        try:
            response = self.xianyu.send_message(account, conversation, message.content)
            trace_id = str(response.get("trace_id") or response.get("message_id") or "")
            self.message_service.mark_sent(message)
            if trace_id:
                message.trace_id = trace_id
        except Exception as exc:
            self.message_service.mark_send_failed(message, str(exc))
        self.session.flush()
        return message

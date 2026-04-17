from __future__ import annotations

from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from domain.message.models import Message


class MessageRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _coerce_uuid(message_id: UUID | str) -> UUID:
        return message_id if isinstance(message_id, UUID) else UUID(str(message_id))

    def get(self, message_id: UUID | str) -> Message | None:
        stmt = select(Message).where(Message.id == self._coerce_uuid(message_id))
        return self.session.scalar(stmt)

    def get_by_external_message_id(self, external_message_id: str) -> Message | None:
        stmt = select(Message).where(Message.external_message_id == external_message_id)
        return self.session.scalar(stmt)

    def save(self, message: Message) -> Message:
        self.session.add(message)
        self.session.flush()
        return message

    def list_by_conversation(self, conversation_id: UUID) -> list[Message]:
        stmt = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
        return list(self.session.scalars(stmt).all())

    def list_recent(self, limit: int = 50, offset: int = 0) -> list[Message]:
        stmt = select(Message).order_by(desc(Message.created_at)).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

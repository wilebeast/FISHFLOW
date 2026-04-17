from __future__ import annotations

from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from domain.conversation.models import Conversation


class ConversationRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _coerce_uuid(value: UUID | str) -> UUID:
        return value if isinstance(value, UUID) else UUID(str(value))

    def get(self, conversation_id: UUID | str) -> Conversation | None:
        stmt = select(Conversation).where(Conversation.id == self._coerce_uuid(conversation_id))
        return self.session.scalar(stmt)

    def get_by_external_conversation_id(self, external_conversation_id: str) -> Conversation | None:
        stmt = select(Conversation).where(
            Conversation.external_conversation_id == external_conversation_id
        )
        return self.session.scalar(stmt)

    def list_recent(
        self,
        product_id: UUID | str | None = None,
        handoff_status: str | None = None,
        buyer_id: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Conversation]:
        stmt = select(Conversation)
        if product_id:
            stmt = stmt.where(Conversation.product_id == self._coerce_uuid(product_id))
        if handoff_status:
            stmt = stmt.where(Conversation.handoff_status == handoff_status)
        if buyer_id:
            stmt = stmt.where(Conversation.buyer_id.ilike(f"%{buyer_id}%"))
        stmt = stmt.order_by(desc(Conversation.last_message_at), desc(Conversation.updated_at))
        stmt = stmt.offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

    def save(self, conversation: Conversation) -> Conversation:
        self.session.add(conversation)
        self.session.flush()
        return conversation

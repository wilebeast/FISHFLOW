from __future__ import annotations

from domain.conversation.models import Conversation


class ConversationService:
    @staticmethod
    def handoff(conversation: Conversation) -> Conversation:
        conversation.handoff_status = "human"
        return conversation

    @staticmethod
    def release(conversation: Conversation) -> Conversation:
        conversation.handoff_status = "bot"
        return conversation

    @staticmethod
    def set_tags(conversation: Conversation, tags: list[str]) -> Conversation:
        conversation.tags = {"items": tags}
        return conversation

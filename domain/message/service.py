from __future__ import annotations

from domain.message.enums import ProcessedStatus
from domain.message.models import Message


class MessageService:
    @staticmethod
    def normalize_content(content: str) -> str:
        return " ".join(content.strip().lower().split())

    def mark_processed(self, message: Message) -> Message:
        message.processed_status = ProcessedStatus.PROCESSED.value
        return message

    def mark_failed(self, message: Message) -> Message:
        message.processed_status = ProcessedStatus.FAILED.value
        return message

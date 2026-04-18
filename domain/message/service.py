from __future__ import annotations

import uuid

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

    @staticmethod
    def mark_send_pending(message: Message) -> Message:
        message.send_status = "pending"
        message.send_error = None
        return message

    @staticmethod
    def mark_sent(message: Message) -> Message:
        message.send_status = "sent"
        message.send_error = None
        message.trace_id = str(uuid.uuid4())
        return message

    @staticmethod
    def mark_send_failed(message: Message, error: str) -> Message:
        message.send_status = "failed"
        message.send_error = error
        message.trace_id = str(uuid.uuid4())
        return message

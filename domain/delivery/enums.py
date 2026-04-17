from enum import StrEnum


class DeliveryTaskStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    MANUAL_REVIEW = "manual_review"
    CANCELLED = "cancelled"


class DeliveryType(StrEnum):
    SEND_TEXT = "send_text"
    SEND_LINK = "send_link"
    SEND_CODE = "send_code"
    SEND_FILE_INSTRUCTION = "send_file_instruction"
    MANUAL_REVIEW = "manual_review"

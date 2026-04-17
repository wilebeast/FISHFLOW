from enum import StrEnum


class SenderType(StrEnum):
    BUYER = "buyer"
    SELLER = "seller"
    SYSTEM = "system"
    BOT = "bot"


class ContentType(StrEnum):
    TEXT = "text"
    IMAGE = "image"
    SYSTEM = "system"


class MessageDirection(StrEnum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"


class ProcessedStatus(StrEnum):
    PENDING = "pending"
    PROCESSED = "processed"
    FAILED = "failed"
    IGNORED = "ignored"

from enum import StrEnum


class OrderStatus(StrEnum):
    CREATED = "created"
    AWAITING_PAYMENT = "awaiting_payment"
    PAID = "paid"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUND_PENDING = "refund_pending"
    REFUNDED = "refunded"
    CLOSED = "closed"


class PayStatus(StrEnum):
    UNPAID = "unpaid"
    PAID = "paid"
    REFUNDING = "refunding"
    REFUNDED = "refunded"


class DeliveryStatus(StrEnum):
    NOT_REQUIRED = "not_required"
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    MANUAL_REVIEW = "manual_review"

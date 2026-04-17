from enum import StrEnum


class RuleScope(StrEnum):
    GLOBAL = "global"
    ACCOUNT = "account"
    PRODUCT = "product"


class TriggerType(StrEnum):
    MESSAGE_RECEIVED = "message_received"
    ORDER_PAID = "order_paid"
    DELIVERY_FAILED = "delivery_failed"
    MANUAL_EVENT = "manual_event"


class ActionType(StrEnum):
    REPLY_TEXT = "reply_text"
    REPLY_TEMPLATE = "reply_template"
    REPLY_AI = "reply_ai"
    HANDOFF_HUMAN = "handoff_human"
    TRIGGER_DELIVERY = "trigger_delivery"
    NOTIFY_ADMIN = "notify_admin"
    IGNORE = "ignore"

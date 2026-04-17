from enum import StrEnum


class TemplateType(StrEnum):
    REPLY = "reply"
    FAQ = "faq"
    DELIVERY = "delivery"
    PROMPT = "prompt"


class TemplateOwnerType(StrEnum):
    SYSTEM = "system"
    ACCOUNT = "account"
    PRODUCT = "product"

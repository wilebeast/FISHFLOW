from __future__ import annotations

from domain.delivery.enums import DeliveryType
from domain.delivery.models import DeliveryTask


class DeliveryExecutor:
    def execute(self, task: DeliveryTask) -> str:
        delivery_type = DeliveryType(task.delivery_type)
        payload = task.payload_snapshot
        if delivery_type == DeliveryType.MANUAL_REVIEW:
            raise RuntimeError("manual review delivery type requires operator intervention")
        if delivery_type == DeliveryType.SEND_TEXT:
            return payload.get("content", "")
        if delivery_type == DeliveryType.SEND_LINK:
            return f"link:{payload.get('link', '')}"
        if delivery_type == DeliveryType.SEND_CODE:
            return f"code:{payload.get('card_code', '')}"
        if delivery_type == DeliveryType.SEND_FILE_INSTRUCTION:
            return payload.get("instruction", "")
        raise RuntimeError(f"unsupported delivery type: {task.delivery_type}")

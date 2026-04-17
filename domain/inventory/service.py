from __future__ import annotations

from domain.inventory.models import InventoryItem
from domain.inventory.schemas import InventoryUpdate


class InventoryService:
    @staticmethod
    def apply_update(item: InventoryItem, payload: InventoryUpdate) -> InventoryItem:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(item, field, value)
        return item

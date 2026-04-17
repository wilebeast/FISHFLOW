from __future__ import annotations

from domain.delivery.models import DeliveryTask
from domain.delivery.repository import DeliveryTaskRepository


class DuplicateDeliveryTaskError(ValueError):
    pass


class DeliveryIdempotencyGuard:
    def __init__(self, repository: DeliveryTaskRepository) -> None:
        self.repository = repository

    def ensure_unique(self, idempotency_key: str) -> None:
        existing = self.repository.get_by_idempotency_key(idempotency_key)
        if existing and existing.status in {"pending", "processing", "success"}:
            raise DuplicateDeliveryTaskError(
                f"delivery task already exists for key={idempotency_key} with status={existing.status}"
            )

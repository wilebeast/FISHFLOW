from __future__ import annotations

from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from domain.delivery.enums import DeliveryTaskStatus
from domain.delivery.models import DeliveryTask


class DeliveryTaskRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _coerce_uuid(task_id: UUID | str) -> UUID:
        return task_id if isinstance(task_id, UUID) else UUID(str(task_id))

    def get_by_idempotency_key(self, idempotency_key: str) -> DeliveryTask | None:
        stmt = select(DeliveryTask).where(DeliveryTask.idempotency_key == idempotency_key)
        return self.session.scalar(stmt)

    def get(self, task_id: UUID | str) -> DeliveryTask | None:
        stmt = select(DeliveryTask).where(DeliveryTask.id == self._coerce_uuid(task_id))
        return self.session.scalar(stmt)

    def has_active_task(self, order_id: UUID) -> bool:
        stmt = select(DeliveryTask).where(
            DeliveryTask.order_id == order_id,
            DeliveryTask.status.in_(
                [DeliveryTaskStatus.PENDING.value, DeliveryTaskStatus.PROCESSING.value]
            ),
        )
        return self.session.scalar(stmt) is not None

    def list_recent(self, limit: int = 50, offset: int = 0) -> list[DeliveryTask]:
        stmt = select(DeliveryTask).order_by(desc(DeliveryTask.created_at)).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

    def save(self, task: DeliveryTask) -> DeliveryTask:
        self.session.add(task)
        self.session.flush()
        return task

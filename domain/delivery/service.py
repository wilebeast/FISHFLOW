from __future__ import annotations

from datetime import datetime, timedelta, timezone

from domain.delivery.enums import DeliveryTaskStatus
from domain.delivery.models import DeliveryTask
from domain.delivery.state_machine import DeliveryStateMachine


class DeliveryTaskService:
    def __init__(self) -> None:
        self.state_machine = DeliveryStateMachine()

    def start(self, task: DeliveryTask) -> DeliveryTask:
        task.status = self.state_machine.transition(
            DeliveryTaskStatus(task.status), DeliveryTaskStatus.PROCESSING
        ).value
        task.attempt_count += 1
        return task

    def mark_success(self, task: DeliveryTask, result_message: str) -> DeliveryTask:
        task.status = self.state_machine.transition(
            DeliveryTaskStatus(task.status), DeliveryTaskStatus.SUCCESS
        ).value
        task.result_message = result_message
        task.executed_at = datetime.now(timezone.utc)
        return task

    def mark_failed(self, task: DeliveryTask, error_message: str, retry_after_seconds: int) -> DeliveryTask:
        task.status = self.state_machine.transition(
            DeliveryTaskStatus(task.status), DeliveryTaskStatus.FAILED
        ).value
        task.last_error = error_message
        task.next_retry_at = datetime.now(timezone.utc) + timedelta(seconds=retry_after_seconds)
        return task

    def requeue_or_escalate(self, task: DeliveryTask) -> DeliveryTask:
        current = DeliveryTaskStatus(task.status)
        if task.attempt_count >= task.max_attempts:
            task.status = self.state_machine.transition(
                current, DeliveryTaskStatus.MANUAL_REVIEW
            ).value
            return task
        task.status = self.state_machine.transition(current, DeliveryTaskStatus.PENDING).value
        return task

    def reset_for_retry(self, task: DeliveryTask) -> DeliveryTask:
        task.status = DeliveryTaskStatus.PENDING.value
        task.last_error = None
        task.result_message = None
        task.next_retry_at = None
        task.executed_at = None
        return task

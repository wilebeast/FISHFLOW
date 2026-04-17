from __future__ import annotations

from domain.delivery.enums import DeliveryTaskStatus


class DeliveryStateError(ValueError):
    pass


class DeliveryStateMachine:
    _allowed_transitions: dict[DeliveryTaskStatus, set[DeliveryTaskStatus]] = {
        DeliveryTaskStatus.PENDING: {
            DeliveryTaskStatus.PROCESSING,
            DeliveryTaskStatus.CANCELLED,
        },
        DeliveryTaskStatus.PROCESSING: {
            DeliveryTaskStatus.SUCCESS,
            DeliveryTaskStatus.FAILED,
        },
        DeliveryTaskStatus.FAILED: {
            DeliveryTaskStatus.PENDING,
            DeliveryTaskStatus.MANUAL_REVIEW,
        },
    }

    def transition(
        self, current: DeliveryTaskStatus, target: DeliveryTaskStatus
    ) -> DeliveryTaskStatus:
        if current == target:
            return current
        if target not in self._allowed_transitions.get(current, set()):
            raise DeliveryStateError(f"invalid delivery transition: {current} -> {target}")
        return target

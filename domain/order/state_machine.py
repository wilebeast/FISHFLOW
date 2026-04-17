from __future__ import annotations

from collections.abc import Iterable

from domain.delivery.enums import DeliveryTaskStatus
from domain.order.enums import DeliveryStatus, OrderStatus, PayStatus


class OrderStateError(ValueError):
    pass


class OrderStateMachine:
    _allowed_transitions: dict[OrderStatus, set[OrderStatus]] = {
        OrderStatus.CREATED: {OrderStatus.AWAITING_PAYMENT},
        OrderStatus.AWAITING_PAYMENT: {
            OrderStatus.PAID,
            OrderStatus.CANCELLED,
        },
        OrderStatus.PAID: {
            OrderStatus.DELIVERING,
            OrderStatus.REFUND_PENDING,
            OrderStatus.CLOSED,
        },
        OrderStatus.DELIVERING: {
            OrderStatus.DELIVERED,
            OrderStatus.CLOSED,
        },
        OrderStatus.DELIVERED: {
            OrderStatus.COMPLETED,
            OrderStatus.REFUND_PENDING,
        },
        OrderStatus.REFUND_PENDING: {OrderStatus.REFUNDED},
    }

    def transition(self, current: OrderStatus, target: OrderStatus) -> OrderStatus:
        if current == target:
            return current
        if target not in self._allowed_transitions.get(current, set()):
            raise OrderStateError(f"invalid order transition: {current} -> {target}")
        return target

    def apply_delivery_result(
        self,
        order_status: OrderStatus,
        delivery_status: DeliveryStatus,
        task_status: DeliveryTaskStatus,
    ) -> tuple[OrderStatus, DeliveryStatus]:
        if task_status == DeliveryTaskStatus.PROCESSING and order_status == OrderStatus.PAID:
            return OrderStatus.DELIVERING, DeliveryStatus.PROCESSING
        if task_status == DeliveryTaskStatus.SUCCESS and order_status == OrderStatus.DELIVERING:
            return OrderStatus.DELIVERED, DeliveryStatus.SUCCESS
        if task_status == DeliveryTaskStatus.FAILED:
            return order_status, DeliveryStatus.FAILED
        if task_status == DeliveryTaskStatus.MANUAL_REVIEW:
            return order_status, DeliveryStatus.MANUAL_REVIEW
        return order_status, delivery_status

    @staticmethod
    def can_start_delivery(order_status: OrderStatus, pay_status: PayStatus) -> bool:
        return order_status == OrderStatus.PAID and pay_status == PayStatus.PAID

    @staticmethod
    def blocks_new_delivery(order_status: OrderStatus) -> bool:
        blocked: Iterable[OrderStatus] = (
            OrderStatus.REFUND_PENDING,
            OrderStatus.REFUNDED,
            OrderStatus.CLOSED,
            OrderStatus.CANCELLED,
        )
        return order_status in blocked

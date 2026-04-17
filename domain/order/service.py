from __future__ import annotations

from datetime import datetime, timezone

from domain.delivery.enums import DeliveryTaskStatus
from domain.order.enums import DeliveryStatus, OrderStatus, PayStatus
from domain.order.models import Order
from domain.order.state_machine import OrderStateMachine


class OrderService:
    def __init__(self) -> None:
        self.state_machine = OrderStateMachine()

    def mark_paid(self, order: Order) -> Order:
        order.order_status = self.state_machine.transition(
            OrderStatus(order.order_status), OrderStatus.PAID
        ).value
        order.pay_status = PayStatus.PAID.value
        order.delivery_status = DeliveryStatus.PENDING.value
        order.paid_at = datetime.now(timezone.utc)
        return order

    def apply_delivery_progress(
        self,
        order: Order,
        delivery_task_status: str,
    ) -> Order:
        next_order_status, next_delivery_status = self.state_machine.apply_delivery_result(
            OrderStatus(order.order_status),
            DeliveryStatus(order.delivery_status),
            DeliveryTaskStatus(delivery_task_status),
        )
        order.order_status = next_order_status.value
        order.delivery_status = next_delivery_status.value
        if next_order_status == OrderStatus.DELIVERED:
            order.delivered_at = datetime.now(timezone.utc)
        return order

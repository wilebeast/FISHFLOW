from __future__ import annotations

from celery import chain

from apps.worker.celery_app import celery_app
from apps.worker.tasks_delivery import create_task_for_paid_order, execute_task


@celery_app.task(name="orders.handle_paid_event")
def handle_paid_event(order_id: str, product_auto_delivery: bool = True) -> str:
    idempotency_key = f"{order_id}:send_text:v1"
    workflow = chain(
        create_task_for_paid_order.s(order_id, product_auto_delivery, idempotency_key),
        execute_task.s(),
    )
    async_result = workflow.apply_async()
    return async_result.id

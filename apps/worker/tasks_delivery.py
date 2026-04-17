from __future__ import annotations

from celery import chain

from apps.worker.celery_app import celery_app
from infrastructure.db.session import SessionLocal
from services.delivery_service.orchestrator import DeliveryOrchestrator


@celery_app.task(name="delivery.create_task_for_paid_order")
def create_task_for_paid_order(order_id: str, product_auto_delivery: bool, idempotency_key: str) -> str:
    session = SessionLocal()
    try:
        orchestrator = DeliveryOrchestrator(session)
        task = orchestrator.create_task_for_order_id(order_id, product_auto_delivery, idempotency_key)
        session.commit()
        return str(task.id)
    finally:
        session.close()


@celery_app.task(name="delivery.execute_task")
def execute_task(task_id: str) -> str:
    session = SessionLocal()
    try:
        orchestrator = DeliveryOrchestrator(session)
        task = orchestrator.execute_task_by_id(task_id)
        session.commit()
        return task.status
    finally:
        session.close()


@celery_app.task(name="delivery.retry_task")
def retry_task(task_id: str) -> str:
    session = SessionLocal()
    try:
        orchestrator = DeliveryOrchestrator(session)
        task = orchestrator.retry_task_by_id(task_id)
        session.commit()
        return task.status
    finally:
        session.close()

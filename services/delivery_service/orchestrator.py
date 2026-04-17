from __future__ import annotations

from sqlalchemy.orm import Session

from domain.delivery.enums import DeliveryType
from domain.delivery.models import DeliveryTask
from domain.delivery.repository import DeliveryTaskRepository
from domain.delivery.schemas import DeliveryTaskCreate
from domain.delivery.service import DeliveryTaskService
from domain.order.models import Order
from domain.order.repository import OrderRepository
from domain.order.service import OrderService
from domain.order.state_machine import OrderStateMachine
from domain.rule.repository import RuleRepository
from domain.template.models import Template
from domain.template.repository import TemplateRepository
from domain.template.service import TemplateService
from services.delivery_service.executor import DeliveryExecutor
from services.delivery_service.idempotency import DeliveryIdempotencyGuard
from services.rule_engine.engine import RuleEngine


class DeliveryOrchestrator:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.order_repository = OrderRepository(session)
        self.delivery_repository = DeliveryTaskRepository(session)
        self.rule_repository = RuleRepository(session)
        self.template_repository = TemplateRepository(session)
        self.order_service = OrderService()
        self.delivery_service = DeliveryTaskService()
        self.order_state_machine = OrderStateMachine()
        self.rule_engine = RuleEngine()
        self.idempotency_guard = DeliveryIdempotencyGuard(self.delivery_repository)
        self.executor = DeliveryExecutor()

    def create_task_for_paid_order(
        self,
        order: Order,
        product_auto_delivery: bool,
        idempotency_key: str,
    ) -> DeliveryTask:
        if not self.order_state_machine.can_start_delivery(
            order_status=order.order_status_enum,
            pay_status=order.pay_status_enum,
        ):
            raise ValueError(f"order {order.external_order_id} is not ready for delivery")
        if self.order_state_machine.blocks_new_delivery(order.order_status_enum):
            raise ValueError(f"order {order.external_order_id} does not allow new delivery")
        self.idempotency_guard.ensure_unique(idempotency_key)

        rules = self.rule_repository.list_enabled("order_paid")
        context = {
            "event": "order_paid",
            "pay_status": order.pay_status,
            "order_status": order.order_status,
            "product_auto_delivery": product_auto_delivery,
        }
        matched_rule = self.rule_engine.match(rules, context)
        if matched_rule is None:
            raise ValueError("no delivery rule matched paid order")

        template = None
        template_id = matched_rule.action_payload.get("template_id")
        if template_id:
            template = self.template_repository.get(template_id)

        payload_snapshot = self._build_payload_snapshot(matched_rule.action_payload, template)
        create = DeliveryTaskCreate(
            order_id=order.id,
            product_id=order.product_id,
            account_id=order.account_id,
            delivery_type=DeliveryType(matched_rule.action_payload["delivery_type"]),
            template_id=template.id if template else None,
            payload_snapshot=payload_snapshot,
            max_attempts=matched_rule.action_payload.get("max_attempts", 3),
            idempotency_key=idempotency_key,
        )
        task = DeliveryTask(**create.model_dump())
        self.delivery_repository.save(task)
        self.session.flush()
        return task

    def create_task_for_order_id(
        self,
        order_id: str,
        product_auto_delivery: bool,
        idempotency_key: str,
    ) -> DeliveryTask:
        order = self.order_repository.get(order_id)
        if order is None:
            raise ValueError(f"order not found: {order_id}")
        return self.create_task_for_paid_order(order, product_auto_delivery, idempotency_key)

    def execute_task(self, order: Order, task: DeliveryTask, retry_after_seconds: int = 120) -> DeliveryTask:
        self.delivery_service.start(task)
        self.order_service.apply_delivery_progress(order, task.status)

        try:
            result_message = self.executor.execute(task)
        except Exception as exc:
            self.delivery_service.mark_failed(task, str(exc), retry_after_seconds)
            self.order_service.apply_delivery_progress(order, task.status)
            self.delivery_service.requeue_or_escalate(task)
            self.order_service.apply_delivery_progress(order, task.status)
            self.session.flush()
            raise

        self.delivery_service.mark_success(task, result_message)
        self.order_service.apply_delivery_progress(order, task.status)
        self.session.flush()
        return task

    def execute_task_by_id(self, task_id: str, retry_after_seconds: int = 120) -> DeliveryTask:
        task = self.delivery_repository.get(task_id)
        if task is None:
            raise ValueError(f"delivery task not found: {task_id}")
        order = self.order_repository.get(task.order_id)
        if order is None:
            raise ValueError(f"order not found for task: {task_id}")
        return self.execute_task(order, task, retry_after_seconds)

    def retry_task_by_id(self, task_id: str, retry_after_seconds: int = 120) -> DeliveryTask:
        task = self.delivery_repository.get(task_id)
        if task is None:
            raise ValueError(f"delivery task not found: {task_id}")
        if task.status == "success":
            raise ValueError(f"delivery task already succeeded: {task_id}")
        self.delivery_service.reset_for_retry(task)
        order = self.order_repository.get(task.order_id)
        if order is None:
            raise ValueError(f"order not found for task: {task_id}")
        self.session.flush()
        return self.execute_task(order, task, retry_after_seconds)

    def _build_payload_snapshot(self, action_payload: dict, template: Template | None) -> dict:
        payload = dict(action_payload)
        if template:
            rendered = TemplateService.render(template, payload.get("variables", {}))
            payload["rendered_content"] = rendered
            payload.setdefault("content", rendered)
        return payload

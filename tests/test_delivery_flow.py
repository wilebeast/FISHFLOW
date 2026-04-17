from __future__ import annotations

from domain.account.models import Account
from domain.conversation.models import Conversation
from domain.delivery.repository import DeliveryTaskRepository
from domain.order.enums import DeliveryStatus, OrderStatus, PayStatus
from domain.order.models import Order
from domain.order.service import OrderService
from domain.product.models import Product
from domain.rule.models import Rule
from domain.template.models import Template
from services.delivery_service.orchestrator import DeliveryOrchestrator


def test_paid_order_delivery_flow_updates_order_and_delivery_task(db_session) -> None:
    account = Account(nickname="seller", external_account_id="acc_001")
    db_session.add(account)
    db_session.flush()

    product = Product(
        account_id=account.id,
        external_product_id="prod_001",
        title="demo",
        delivery_mode="auto",
    )
    conversation = Conversation(
        account_id=account.id,
        product_id=product.id,
        external_conversation_id="conv_001",
    )
    db_session.add_all([product, conversation])
    db_session.flush()

    template = Template(
        template_type="delivery",
        name="delivery_tpl",
        owner_type="system",
        content="链接：{{delivery_content}}",
    )
    db_session.add(template)
    db_session.flush()

    rule = Rule(
        name="paid delivery",
        scope="global",
        trigger_type="order_paid",
        conditions={
            "event": "order_paid",
            "require_payment_status": "paid",
            "require_product_auto_delivery": True,
            "exclude_order_status": ["refund_pending", "refunded", "closed"],
        },
        action_type="trigger_delivery",
        action_payload={
            "delivery_type": "send_text",
            "template_id": str(template.id),
            "variables": {"delivery_content": "https://example.com/dl"},
            "max_attempts": 3,
        },
    )
    db_session.add(rule)

    order = Order(
        account_id=account.id,
        product_id=product.id,
        conversation_id=conversation.id,
        external_order_id="order_001",
        amount=19.9,
        order_status=OrderStatus.AWAITING_PAYMENT.value,
        pay_status=PayStatus.UNPAID.value,
        delivery_status=DeliveryStatus.PENDING.value,
    )
    db_session.add(order)
    db_session.flush()

    OrderService().mark_paid(order)
    orchestrator = DeliveryOrchestrator(db_session)
    task = orchestrator.create_task_for_paid_order(
        order=order,
        product_auto_delivery=True,
        idempotency_key=f"{order.id}:send_text:v1",
    )
    orchestrator.execute_task(order, task)
    db_session.commit()

    db_session.refresh(order)
    db_session.refresh(task)

    assert order.order_status == OrderStatus.DELIVERED.value
    assert order.delivery_status == DeliveryStatus.SUCCESS.value
    assert task.status == "success"
    assert "https://example.com/dl" in task.result_message
    assert DeliveryTaskRepository(db_session).has_active_task(order.id) is False

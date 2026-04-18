from infrastructure.db.session import SessionLocal
from datetime import date

from infrastructure.db.models import (
    AICopyHistory,
    AIReplyConfig,
    Account,
    AnalyticsSnapshot,
    AppSetting,
    Conversation,
    InventoryItem,
    KnowledgeItem,
    NotificationConfig,
    Product,
    Rule,
    Template,
)


def main() -> None:
    session = SessionLocal()
    try:
        account = session.query(Account).filter_by(external_account_id="acc_demo_001").one_or_none()
        if account is None:
            account = Account(
                nickname="FishFlow Demo Seller",
                external_account_id="acc_demo_001",
                risk_level="low",
            )
            session.add(account)
            session.flush()

        product = session.query(Product).filter_by(external_product_id="prod_demo_001").one_or_none()
        if product is None:
            product = Product(
                account_id=account.id,
                external_product_id="prod_demo_001",
                title="演示版数字商品",
                category="digital",
                price=19.90,
                delivery_mode="auto",
                auto_delivery_enabled=True,
            )
            session.add(product)
            session.flush()

        conversation = (
            session.query(Conversation)
            .filter_by(external_conversation_id="conv_demo_001")
            .one_or_none()
        )
        if conversation is None:
            conversation = Conversation(
                account_id=account.id,
                product_id=product.id,
                external_conversation_id="conv_demo_001",
                buyer_id="buyer_demo_001",
            )
            session.add(conversation)
            session.flush()

        template = session.query(Template).filter_by(name="默认自动发货模板").one_or_none()
        if template is None:
            template = Template(
                template_type="delivery",
                name="默认自动发货模板",
                owner_type="system",
                description="系统默认演示发货模板",
                category="delivery",
                content="您好，您购买的内容如下：{{delivery_content}}",
                variables={"delivery_content": "演示资源链接：https://example.com/download/demo"},
                is_default=True,
            )
            session.add(template)
            session.flush()

        faq_template = session.query(Template).filter_by(name="默认 FAQ 模板").one_or_none()
        if faq_template is None:
            faq_template = Template(
                template_type="faq",
                name="默认 FAQ 模板",
                owner_type="system",
                description="系统默认 FAQ 模板",
                category="faq",
                content="常见问题：付款后自动发货，若失败请联系人工处理。",
                variables={},
                is_default=True,
            )
            session.add(faq_template)
            session.flush()

        rule = session.query(Rule).filter_by(name="支付后默认自动发货").one_or_none()
        if rule is None:
            rule = Rule(
                name="支付后默认自动发货",
                scope="global",
                trigger_type="order_paid",
                priority=100,
                enabled=True,
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
                    "variables": {
                        "delivery_content": "演示资源链接：https://example.com/download/demo"
                    },
                    "max_attempts": 3,
                },
            )
            session.add(rule)
            session.flush()

        if product.delivery_template_id is None:
            product.delivery_template_id = template.id
        if product.faq_template_id is None:
            product.faq_template_id = faq_template.id
        if product.rule_profile_id is None:
            product.rule_profile_id = rule.id

        greeting_rule = session.query(Rule).filter_by(name="买家问候自动回复").one_or_none()
        if greeting_rule is None:
            greeting_rule = Rule(
                name="买家问候自动回复",
                scope="global",
                trigger_type="message_received",
                priority=90,
                enabled=True,
                conditions={"event": "message_received", "contains": "你好"},
                action_type="reply_text",
                action_payload={"content": "您好，在的，付款后自动发货。"},
            )
            session.add(greeting_rule)

        inventory_item = session.query(InventoryItem).filter_by(code="CARD-DEMO-001").one_or_none()
        if inventory_item is None:
            inventory_item = InventoryItem(
                resource_type="card",
                product_id=product.id,
                code="CARD-DEMO-001",
                content="演示卡密：XXXX-YYYY-ZZZZ",
                note="seed demo card",
            )
            session.add(inventory_item)

        notification_config = session.query(NotificationConfig).filter_by(name="默认 Webhook 通知").one_or_none()
        if notification_config is None:
            notification_config = NotificationConfig(
                channel="webhook",
                name="默认 Webhook 通知",
                target="https://example.com/webhook/fishflow",
                config_json={"headers": {"X-Demo": "fishflow"}},
                enabled=True,
            )
            session.add(notification_config)

        ai_reply_config = session.query(AIReplyConfig).filter_by(name="default").one_or_none()
        if ai_reply_config is None:
            ai_reply_config = AIReplyConfig(
                name="default",
                provider="openai-compatible",
                model="gpt-5-mini",
                system_prompt="You are a concise sales assistant for FishFlow demos.",
                temperature=0.2,
                max_tokens=200,
                enabled=True,
                guardrails_json={
                    "forbidden_claims": ["guaranteed profit", "permanent support"],
                    "handoff_keywords": ["退款", "投诉"],
                },
            )
            session.add(ai_reply_config)

        knowledge_item = session.query(KnowledgeItem).filter_by(question="怎么发货？").one_or_none()
        if knowledge_item is None:
            knowledge_item = KnowledgeItem(
                product_id=product.id,
                category="faq",
                question="怎么发货？",
                answer="付款后系统自动发货，如异常会转人工处理。",
                tags={"scene": "delivery"},
                enabled=True,
            )
            session.add(knowledge_item)

        analytics_snapshot = session.query(AnalyticsSnapshot).filter_by(snapshot_date=date.today()).one_or_none()
        if analytics_snapshot is None:
            analytics_snapshot = AnalyticsSnapshot(
                snapshot_date=date.today(),
                message_count=12,
                auto_reply_count=9,
                handoff_count=2,
                delivery_success_count=5,
                delivery_fail_count=1,
            )
            session.add(analytics_snapshot)

        app_setting = session.query(AppSetting).filter_by(key="app.branding").one_or_none()
        if app_setting is None:
            app_setting = AppSetting(
                key="app.branding",
                value_json={"name": "FishFlow", "mode": "demo", "theme": "sand"},
            )
            session.add(app_setting)

        copy_history = session.query(AICopyHistory).filter_by(scene="title").one_or_none()
        if copy_history is None:
            copy_history = AICopyHistory(
                scene="title",
                input_payload={"product_title": "演示版数字商品"},
                output_payload={"content": "闲鱼热卖 | 演示版数字商品 | 自动发货"},
                operator="seed",
            )
            session.add(copy_history)

        session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    main()

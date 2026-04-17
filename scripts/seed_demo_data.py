from infrastructure.db.session import SessionLocal
from infrastructure.db.models import Account, Conversation, Product, Rule, Template


def main() -> None:
    session = SessionLocal()
    try:
        account = session.query(Account).filter_by(external_account_id="acc_demo_001").one_or_none()
        if account is None:
            account = Account(nickname="FishFlow Demo Seller", external_account_id="acc_demo_001")
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

        session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    main()

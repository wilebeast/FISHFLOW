from __future__ import annotations

from domain.account.models import Account
from domain.conversation.models import Conversation
from domain.message.enums import MessageDirection, ProcessedStatus, SenderType
from domain.message.repository import MessageRepository
from domain.message.schemas import MessageCreate
from domain.product.models import Product
from domain.rule.models import Rule
from services.message_service.processor import MessageProcessor


def test_message_ingest_and_auto_reply(db_session) -> None:
    account = Account(nickname="seller", external_account_id="acc_msg")
    db_session.add(account)
    db_session.flush()

    product = Product(account_id=account.id, external_product_id="prod_msg", title="msg demo")
    db_session.add(product)
    db_session.flush()

    conversation = Conversation(
        account_id=account.id,
        product_id=product.id,
        external_conversation_id="conv_msg",
        buyer_id="buyer_001",
    )
    db_session.add(conversation)
    db_session.flush()

    rule = Rule(
        name="hello auto reply",
        scope="global",
        trigger_type="message_received",
        conditions={"event": "message_received", "contains": "你好"},
        action_type="reply_text",
        action_payload={"content": "您好，在的，付款后自动发货。"},
    )
    db_session.add(rule)
    db_session.commit()

    processor = MessageProcessor(db_session)
    inbound = processor.ingest_message(
        MessageCreate(
            conversation_id=conversation.id,
            external_message_id="msg_ext_001",
            sender_type=SenderType.BUYER,
            content=" 你好 在吗 ",
            direction=MessageDirection.INBOUND,
        )
    )
    db_session.commit()

    processed, reply, route = processor.process_inbound_message(str(inbound.id))
    db_session.commit()

    repo = MessageRepository(db_session)
    messages = repo.list_by_conversation(conversation.id)

    assert processed.processed_status == ProcessedStatus.PROCESSED.value
    assert route.action_type == "reply_text"
    assert reply is not None
    assert reply.direction == MessageDirection.OUTBOUND.value
    assert reply.content == "您好，在的，付款后自动发货。"
    assert len(messages) == 2

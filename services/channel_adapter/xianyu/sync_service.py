from __future__ import annotations

import asyncio

from sqlalchemy.orm import Session

from domain.account.models import Account
from domain.conversation.models import Conversation
from domain.order.enums import DeliveryStatus, OrderStatus, PayStatus
from domain.order.models import Order
from domain.order.repository import OrderRepository
from domain.product.models import Product
from domain.product.repository import ProductRepository
from services.channel_adapter.xianyu.message_adapter import XianyuMessageAdapter
from services.channel_adapter.xianyu.order_adapter import XianyuOrderAdapter
from services.channel_adapter.xianyu.product_adapter import XianyuProductAdapter


def _parse_price(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


class XianyuSyncService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.products = ProductRepository(session)
        self.orders = OrderRepository(session)
        self.message_adapter = XianyuMessageAdapter()
        self.order_adapter = XianyuOrderAdapter()
        self.product_adapter = XianyuProductAdapter()

    def send_message(self, account: Account, conversation: Conversation, content: str) -> dict:
        return asyncio.run(
            self.message_adapter.send_message(
                account_ref=account.external_account_id,
                session_ref=conversation.external_conversation_id,
                content=content,
            )
        )

    def sync_products(self, account: Account) -> int:
        items = asyncio.run(self.product_adapter.fetch_products(account.external_account_id))
        synced = 0
        for item in items:
            external_product_id = str(item.get("id") or item.get("external_product_id") or "").strip()
            if not external_product_id:
                continue
            product = self.products.get_by_external_product_id(external_product_id)
            if product is None:
                product = Product(
                    account_id=account.id,
                    external_product_id=external_product_id,
                    title=item.get("title") or f"Xianyu Product {external_product_id}",
                )
                self.products.save(product)
            product.account_id = account.id
            product.title = item.get("title") or product.title
            product.category = item.get("category") or product.category
            product.price = _parse_price(item.get("price"))
            product.delivery_mode = item.get("delivery_mode") or product.delivery_mode
            product.status = item.get("status") or product.status
            synced += 1
        self.session.flush()
        return synced

    def sync_orders(self, account: Account) -> int:
        items = asyncio.run(self.order_adapter.fetch_orders(account.external_account_id))
        synced = 0
        for item in items:
            external_order_id = str(item.get("id") or item.get("external_order_id") or "").strip()
            if not external_order_id:
                continue

            order = self.orders.get_by_external_order_id(external_order_id)
            if order is None:
                order = Order(
                    account_id=account.id,
                    external_order_id=external_order_id,
                    amount=_parse_price(item.get("amount")),
                )
                self.orders.save(order)

            product_ref = item.get("product_id")
            linked_product = self.products.get_by_external_product_id(str(product_ref)) if product_ref else None

            order.account_id = account.id
            order.product_id = linked_product.id if linked_product else order.product_id
            order.buyer_id = item.get("buyer_id") or order.buyer_id
            order.amount = _parse_price(item.get("amount"))
            order.currency = item.get("currency") or order.currency
            order.order_status = item.get("order_status") or order.order_status or OrderStatus.CREATED.value
            order.pay_status = item.get("pay_status") or order.pay_status or PayStatus.UNPAID.value
            order.delivery_status = (
                item.get("delivery_status") or order.delivery_status or DeliveryStatus.PENDING.value
            )
            order.metadata_json = item
            synced += 1
        self.session.flush()
        return synced

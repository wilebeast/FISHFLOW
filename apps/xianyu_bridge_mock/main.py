from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Query
from pydantic import BaseModel


app = FastAPI(title="FishFlow Xianyu Bridge Mock", version="0.1.0")

MOCK_TOKEN = "bridge-demo-token"


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def require_auth(authorization: str | None) -> None:
    if not authorization:
        return
    if authorization != f"Bearer {MOCK_TOKEN}":
        raise HTTPException(status_code=401, detail="invalid bridge token")


MOCK_PRODUCTS: dict[str, list[dict[str, Any]]] = {
    "acc_demo_001": [
        {
            "id": "x_prod_001",
            "external_product_id": "x_prod_001",
            "title": "闲鱼虚拟资料包",
            "category": "digital",
            "price": 19.9,
            "delivery_mode": "auto",
            "status": "active",
        },
        {
            "id": "x_prod_002",
            "external_product_id": "x_prod_002",
            "title": "简历模板合集",
            "category": "template",
            "price": 9.9,
            "delivery_mode": "manual",
            "status": "active",
        },
    ]
}

MOCK_ORDERS: dict[str, list[dict[str, Any]]] = {
    "acc_demo_001": [
        {
            "id": "x_order_001",
            "external_order_id": "x_order_001",
            "product_id": "x_prod_001",
            "buyer_id": "buyer_sync_001",
            "amount": 19.9,
            "currency": "CNY",
            "order_status": "paid",
            "pay_status": "paid",
            "delivery_status": "pending",
            "created_at": utcnow(),
        },
        {
            "id": "x_order_002",
            "external_order_id": "x_order_002",
            "product_id": "x_prod_002",
            "buyer_id": "buyer_sync_002",
            "amount": 9.9,
            "currency": "CNY",
            "order_status": "awaiting_payment",
            "pay_status": "unpaid",
            "delivery_status": "pending",
            "created_at": utcnow(),
        },
    ]
}

MOCK_MESSAGES: dict[str, list[dict[str, Any]]] = {
    "acc_demo_001": [
        {
            "id": "x_msg_001",
            "external_message_id": "x_msg_001",
            "session": "conv_demo_001",
            "sender": "buyer",
            "content": "你好，在吗",
            "created_at": utcnow(),
        }
    ]
}


class SendMessagePayload(BaseModel):
    account: str
    session: str
    content: str


@app.get("/")
def root() -> dict[str, str]:
    return {"service": app.title, "version": app.version}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "xianyu-bridge-mock"}


@app.get("/messages")
def list_messages(
    account: str = Query(...),
    cursor: str | None = Query(default=None),
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    require_auth(authorization)
    items = MOCK_MESSAGES.get(account, [])
    return {"items": items, "next_cursor": cursor}


@app.post("/messages/send")
def send_message(
    payload: SendMessagePayload,
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    require_auth(authorization)
    message_id = f"mock_sent_{len(MOCK_MESSAGES.get(payload.account, [])) + 1:03d}"
    item = {
        "id": message_id,
        "external_message_id": message_id,
        "session": payload.session,
        "sender": "seller",
        "content": payload.content,
        "created_at": utcnow(),
    }
    MOCK_MESSAGES.setdefault(payload.account, []).append(item)
    return {"status": "sent", "message_id": message_id, "trace_id": f"trace_{message_id}"}


@app.get("/orders")
def list_orders(
    account: str = Query(...),
    cursor: str | None = Query(default=None),
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    require_auth(authorization)
    return {"items": MOCK_ORDERS.get(account, []), "next_cursor": cursor}


@app.get("/orders/detail")
def order_detail(
    account: str = Query(...),
    order: str = Query(...),
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    require_auth(authorization)
    for item in MOCK_ORDERS.get(account, []):
        if item["id"] == order or item["external_order_id"] == order:
            return item
    raise HTTPException(status_code=404, detail="order not found")


@app.get("/products")
def list_products(
    account: str = Query(...),
    cursor: str | None = Query(default=None),
    authorization: str | None = Header(default=None),
) -> dict[str, Any]:
    require_auth(authorization)
    return {"items": MOCK_PRODUCTS.get(account, []), "next_cursor": cursor}

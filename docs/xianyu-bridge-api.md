# Xianyu Bridge API

FishFlow 不直接内置闲鱼私有协议，而是通过一个桥接服务完成真实平台交互。

当前 FishFlow 已接入的桥接能力有三类：

1. 发送卖家消息
2. 同步订单
3. 同步商品

Bridge 还可以把闲鱼入站消息推送回 FishFlow 的事件入口。

## 配置项

FishFlow 通过以下环境变量连接 Bridge：

```env
XIANYU_BRIDGE_API_BASE_URL=http://127.0.0.1:8787
XIANYU_BRIDGE_TOKEN=
XIANYU_TIMEOUT_SECONDS=15
```

如果配置了 `XIANYU_BRIDGE_TOKEN`，FishFlow 会在请求头里携带：

```http
Authorization: Bearer <token>
```

## 请求约定

### 1. POST `/messages/send`

用途：
FishFlow 触发手动发送消息或自动回复时调用。

请求体：

```json
{
  "account": "acc_demo_001",
  "session": "conv_demo_001",
  "content": "您好，付款后自动发货。"
}
```

返回建议：

```json
{
  "status": "sent",
  "message_id": "mock_sent_001",
  "trace_id": "trace_mock_sent_001"
}
```

字段说明：
- `account`：FishFlow 中 `accounts.external_account_id`
- `session`：FishFlow 中 `conversations.external_conversation_id`
- `content`：要发送给买家的文本
- `trace_id`：可选，FishFlow 会记录到消息表 `trace_id`

### 2. GET `/orders`

用途：
FishFlow 主动同步账号订单列表。

查询参数：

```text
account=<external_account_id>
cursor=<optional_cursor>
```

返回建议：

```json
{
  "items": [
    {
      "id": "x_order_001",
      "external_order_id": "x_order_001",
      "product_id": "x_prod_001",
      "buyer_id": "buyer_sync_001",
      "amount": 19.9,
      "currency": "CNY",
      "order_status": "paid",
      "pay_status": "paid",
      "delivery_status": "pending"
    }
  ],
  "next_cursor": null
}
```

字段映射建议：
- `product_id` 对应 FishFlow 商品的 `external_product_id`
- `order_status` / `pay_status` / `delivery_status` 直接按 FishFlow 现有枚举值返回

### 3. GET `/orders/detail`

用途：
FishFlow 查询单个订单细节。

查询参数：

```text
account=<external_account_id>
order=<external_order_id>
```

返回建议：

```json
{
  "id": "x_order_001",
  "external_order_id": "x_order_001",
  "product_id": "x_prod_001",
  "buyer_id": "buyer_sync_001",
  "amount": 19.9,
  "currency": "CNY",
  "order_status": "paid",
  "pay_status": "paid",
  "delivery_status": "pending"
}
```

### 4. GET `/products`

用途：
FishFlow 主动同步商品列表。

查询参数：

```text
account=<external_account_id>
cursor=<optional_cursor>
```

返回建议：

```json
{
  "items": [
    {
      "id": "x_prod_001",
      "external_product_id": "x_prod_001",
      "title": "闲鱼虚拟资料包",
      "category": "digital",
      "price": 19.9,
      "delivery_mode": "auto",
      "status": "active"
    }
  ],
  "next_cursor": null
}
```

字段映射建议：
- `id` 或 `external_product_id` 至少返回一个
- `delivery_mode` 建议直接返回 `auto` 或 `manual`
- `status` 建议返回 `active` / `inactive`

### 5. GET `/messages`

用途：
Bridge 拉取入站消息时可提供这个接口；当前 FishFlow 代码里已经为消息适配器预留了调用。

查询参数：

```text
account=<external_account_id>
cursor=<optional_cursor>
```

返回建议：

```json
{
  "items": [
    {
      "id": "x_msg_001",
      "external_message_id": "x_msg_001",
      "session": "conv_demo_001",
      "sender": "buyer",
      "content": "你好，在吗",
      "created_at": "2026-04-18T12:00:00+00:00"
    }
  ],
  "next_cursor": null
}
```

## Bridge 推送 FishFlow 入站消息

如果 Bridge 不做消息轮询提供，也可以反向推送给 FishFlow：

### POST FishFlow `/events/messages/received`

请求体：

```json
{
  "external_conversation_id": "conv_demo_001",
  "external_message_id": "x_msg_101",
  "sender_type": "buyer",
  "content_type": "text",
  "content": "你好，在吗"
}
```

响应：

```json
{
  "status": "accepted",
  "message_id": "4e4e8c34-8d0c-4b0f-b4e8-6d18c5b3d86f",
  "conversation_id": "67e4ed12-7f08-4470-92f9-b7b3e3f6bf75"
}
```

说明：
- 如果你已经知道 FishFlow 的 `conversation_id`，也可以直接传 `conversation_id`
- 如果只传 `external_conversation_id`，FishFlow 会先在本地查找对应会话

## Mock Bridge

仓库内提供了本地联调用的 mock bridge：

```bash
cd /home/star/FishFlow
source .venv/bin/activate
python -m uvicorn apps.xianyu_bridge_mock.main:app --reload --port 8787
```

默认 token：

```text
bridge-demo-token
```

如果你在 `.env` 中配置：

```env
XIANYU_BRIDGE_TOKEN=bridge-demo-token
```

FishFlow 就可以直接用 mock bridge 做本地联调。

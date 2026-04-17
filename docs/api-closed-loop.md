# FishFlow 最小闭环

## 流程

1. 调用 `POST /orders` 创建订单
2. 调用 `POST /orders/{order_id}/mark-paid` 标记订单已支付
3. API 通过后台任务触发 `orders.handle_paid_event`
4. Worker 创建 `delivery_tasks`
5. Worker 执行发货任务并回写 `orders.delivery_status`

## 本地初始化

1. 安装依赖：`pip install -e .`
2. 执行 Alembic 迁移：`alembic upgrade head`
3. 导入演示数据：`python3 scripts/seed_demo_data.py`
4. 启动 API：`uvicorn apps.api.main:app --reload`
5. 启动 Worker：`celery -A apps.worker.celery_app.celery_app worker -l info`

## 演示调用

创建订单：

```bash
curl -X POST http://127.0.0.1:8000/orders \
  -H 'Content-Type: application/json' \
  -d '{
    "external_order_id": "order_demo_api_001",
    "amount": 19.9
  }'
```

标记已支付并触发闭环：

```bash
curl -X POST http://127.0.0.1:8000/orders/{order_id}/mark-paid
```

或直接发送支付事件：

```bash
curl -X POST "http://127.0.0.1:8000/events/orders/paid?order_id={order_id}"
```

## 关键文件

- `infrastructure/db/migrations/versions/20260417_0001_initial_schema.py`
- `deploy/sql/001_initial_schema.sql`
- `deploy/sql/002_seed_demo_data.sql`
- `interfaces/http/routers/orders.py`
- `apps/worker/tasks_order.py`
- `apps/worker/tasks_delivery.py`

# FishFlow

FishFlow 是一个面向闲鱼卖家的自动成交中台 MVP。

当前版本已经打通了三个核心闭环：

- 订单创建与支付后自动发货任务生成
- 买家消息入库、规则匹配与自动回复记录生成
- 后台查看订单、消息、发货任务，并执行最小操作

这不是一个功能完整的商业版，而是一个已经可以本地演示和继续扩展的操作型 MVP。

## 当前能力

### 已完成

- FastAPI API 服务
- Celery 异步任务链路
- PostgreSQL + Alembic 初始迁移
- Redis 作为 Celery broker/backend
- 订单、消息、发货任务三类核心领域模型
- 支付后自动创建 `delivery_tasks`
- 消息入库后自动生成回复记录
- 管理后台最小页面：
  - `Orders`
  - `Messages`
  - `Deliveries`
- 最小集成测试通过

### 当前可演示操作

- 创建订单
- 标记订单已支付
- 注入测试消息
- 查看自动发货任务详情
- 对失败任务执行重试

### 尚未完成

- 闲鱼真实协议接入
- 真实消息发送
- 商品管理与多账号管理
- AI 文案中心
- 权限系统、租户系统、报表系统

## 技术栈

- Backend: Python 3.12, FastAPI, SQLAlchemy, Celery
- Frontend: Next.js 14, React 18
- Database: PostgreSQL
- Queue / Broker: Redis
- Migration: Alembic
- Test: pytest

## 快速开始

### 1. 创建虚拟环境并安装依赖

```bash
cd /home/star/FishFlow
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
python -m pip install -e '.[dev]'
```

### 2. 配置环境变量

复制示例文件并按你的本地 PostgreSQL / Redis 实际情况修改：

```bash
cp .env.example .env
```

重点确认：

- `DATABASE_URL`
- `REDIS_URL`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`

### 3. 执行数据库迁移

```bash
source .venv/bin/activate
python -m alembic upgrade head
```

### 4. 导入演示数据

```bash
source .venv/bin/activate
python scripts/seed_demo_data.py
```

### 5. 启动 API

```bash
source .venv/bin/activate
uvicorn apps.api.main:app --reload
```

服务地址：

- API: `http://127.0.0.1:8000`

### 6. 启动 Worker

```bash
source .venv/bin/activate
celery -A apps.worker.celery_app.celery_app worker -l info
```

### 7. 启动 Admin Web

```bash
cd apps/admin-web
npm install
API_BASE_URL=http://127.0.0.1:8000 npm run dev
```

页面地址：

- Admin: `http://127.0.0.1:3000`

## 演示脚本

### 演示 1：消息自动回复链路

1. 打开 `Messages`
2. 输入会话 ID，例如 `conv_demo_001`
3. 注入消息：`你好，在吗`
4. 刷新列表

预期结果：

- 出现一条买家入站消息
- 出现一条系统自动生成的 bot 出站消息

### 演示 2：支付后发货链路

1. 打开 `Orders`
2. 对未支付订单点击 `Mark Paid`
3. 打开 `Deliveries`
4. 查看新创建的发货任务

预期结果：

- 新任务出现在发货列表
- 可查看 `payload_snapshot`
- 可看到执行结果

## API 概览

### 系统

- `GET /`
- `GET /health`

### 订单

- `GET /orders`
- `POST /orders`
- `GET /orders/{external_order_id}`
- `POST /orders/{order_id}/mark-paid`

### 消息

- `GET /messages`
- `POST /events/messages/received`

### 发货任务

- `GET /deliveries`
- `GET /deliveries/{task_id}`
- `POST /deliveries/{task_id}/retry`

## 测试

```bash
source .venv/bin/activate
python -m pytest -q
```

## Docker

仓库已包含最小 Docker Compose 方案：

```bash
docker compose -f deploy/docker-compose.yml up --build
```

详细说明见：

- `docs/api-closed-loop.md`
- `docs/project-structure.md`

## 项目阶段

当前阶段可以描述为：

**本地可演示的操作型 MVP**

它已经证明核心流程能跑，但还没有进入真实闲鱼联调和商业化可交付阶段。

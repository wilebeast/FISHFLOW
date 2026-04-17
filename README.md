# FishFlow

FishFlow 是一个面向闲鱼卖家的自动成交中台 MVP。

当前版本已经打通了 V0.3 的主链路：

- 订单创建与支付后自动发货任务生成
- 买家消息入库、规则匹配与自动回复记录生成
- 后台管理账号、库存/卡密池、商品、会话、模板、规则、通知、审计、AI 回复配置
- 后台可执行最小操作：人工接管、手动发送消息、规则启停、模板启停、发货重试、账号健康检查、库存分配、通知测试、AI 回复测试

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
  - `Accounts`
  - `Inventory`
  - `Products`
  - `Conversations`
  - `Orders`
  - `Messages`
  - `Deliveries`
  - `Templates`
  - `Rules`
  - `Notifications`
  - `Audit`
  - `AI Reply`
  - `System`
- 最小集成测试通过

### 当前可演示操作

- 创建订单
- 创建账号
- 创建库存项 / 卡密项
- 创建商品
- 标记订单已支付
- 注入测试消息
- 会话人工接管 / 解除接管
- 会话手动发送消息
- 创建模板与启停模板
- 创建规则与启停规则
- 配置通知通道并执行测试
- 配置 AI 回复并生成测试回复
- 查看自动发货任务详情
- 对失败任务执行重试

### 当前 V0.3 仍未完成

- 闲鱼真实协议接入
- 真实消息发送
- AI 文案中心
- 权限系统、租户系统、报表系统
- 真实外部通知发送
- 真实 LLM 集成与计费

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

### 演示 0：账号、库存和通知配置

1. 打开 `Accounts`
2. 创建一个演示账号并执行 `Health Check`
3. 打开 `Inventory`
4. 创建一条卡密或链接库存
5. 打开 `Notifications`
6. 保存通知配置并执行测试

预期结果：

- 账号会更新最近巡检状态
- 库存项会进入列表
- 系统事件会出现一条通知测试记录

### 演示 1：商品和自动化配置

1. 打开 `Products`
2. 创建一个新商品
3. 绑定规则和模板
4. 切换自动发货开关

预期结果：

- 商品出现在列表中
- 自动化绑定关系可在后台直接修改

### 演示 2：消息自动回复链路

1. 打开 `Messages`
2. 输入会话 ID，例如 `conv_demo_001`
3. 注入消息：`你好，在吗`
4. 刷新列表

预期结果：

- 出现一条买家入站消息
- 出现一条系统自动生成的 bot 出站消息

### 演示 3：会话操作链路

1. 打开 `Conversations`
2. 对会话执行 `Handoff`
3. 再执行 `Release`
4. 手动发送一条消息

预期结果：

- 接管状态发生变化
- 会话时间线会增加一条出站消息

### 演示 4：支付后发货链路

1. 打开 `Orders`
2. 对未支付订单点击 `Mark Paid`
3. 打开 `Deliveries`
4. 查看新创建的发货任务

预期结果：

- 新任务出现在发货列表
- 可查看 `payload_snapshot`
- 可看到执行结果

### 演示 5：AI 回复配置

1. 打开 `AI Reply`
2. 保存默认配置
3. 输入一条买家问题并执行测试
4. 查看调用日志

预期结果：

- 页面会返回一条演示 AI 回复
- 日志表会新增一条 AI 调用记录

## API 概览

### 系统

- `GET /`
- `GET /health`

### 订单

- `GET /orders`
- `POST /orders`
- `GET /orders/{external_order_id}`
- `POST /orders/{order_id}/mark-paid`

### 商品

- `GET /products`
- `POST /products`
- `GET /products/{id}`
- `PATCH /products/{id}`
- `POST /products/{id}/bind-rule`
- `POST /products/{id}/bind-delivery-template`
- `POST /products/{id}/bind-faq-template`
- `POST /products/{id}/toggle-auto-delivery`

### 会话

- `GET /conversations`
- `GET /conversations/{id}`
- `GET /conversations/{id}/messages`
- `POST /conversations/{id}/handoff`
- `POST /conversations/{id}/release`
- `POST /conversations/{id}/tags`
- `POST /conversations/{id}/send`

### 消息

- `GET /messages`
- `GET /messages/{id}`
- `POST /messages/{conversation_id}/send`
- `POST /events/messages/received`

### 发货任务

- `GET /deliveries`
- `GET /deliveries/{task_id}`
- `POST /deliveries/{task_id}/retry`

### 模板

- `GET /templates`
- `POST /templates`
- `GET /templates/{id}`
- `PATCH /templates/{id}`

### 规则

- `GET /rules`
- `POST /rules`
- `GET /rules/{id}`
- `PATCH /rules/{id}`
- `POST /rules/{id}/enable`
- `POST /rules/{id}/disable`

### 系统

- `GET /system/health`
- `GET /system/queue`
- `GET /system/errors`

### 账号

- `GET /accounts`
- `POST /accounts`
- `GET /accounts/{id}`
- `PATCH /accounts/{id}`
- `POST /accounts/{id}/health-check`
- `POST /accounts/{id}/disable`

### 库存

- `GET /inventory`
- `POST /inventory`
- `GET /inventory/{id}`
- `PATCH /inventory/{id}`
- `POST /inventory/{id}/allocate`
- `POST /inventory/{id}/disable`

### 通知

- `GET /notifications/config`
- `POST /notifications/config`
- `PATCH /notifications/config/{id}`
- `POST /notifications/test`

### 审计

- `GET /audit/admin-actions`
- `GET /audit/system-events`

### AI 回复

- `GET /ai/reply/config`
- `POST /ai/reply/config`
- `PATCH /ai/reply/config/{id}`
- `POST /ai/reply/test`
- `GET /ai/reply/logs`

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

**本地可演示的操作型 V0.3 MVP**

它已经证明账号、库存、商品、会话、订单、消息、发货任务、规则、模板、通知和 AI 回复配置这几条核心流程能跑，但还没有进入真实闲鱼联调和商业化可交付阶段。

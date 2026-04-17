# FishFlow 项目结构

## 顶层目录

```text
apps/
deploy/
docs/
domain/
infrastructure/
interfaces/
scripts/
services/
tests/
```

## apps

运行入口和应用壳层。

- `apps/api`
  - FastAPI 应用入口
  - 聚合 HTTP 路由
- `apps/worker`
  - Celery worker 入口
  - 订单、消息、发货相关任务
- `apps/admin-web`
  - Next.js 管理后台
  - 当前包含 `Orders / Messages / Deliveries` 最小页面

## domain

领域模型层，描述核心业务对象。

- `account`
- `conversation`
- `delivery`
- `message`
- `order`
- `product`
- `rule`
- `template`

每个领域通常包含：

- `models.py`
- `repository.py`
- `schemas.py`
- `service.py`
- `enums.py`

## services

跨领域业务动作和流程编排。

- `delivery_service`
  - 支付后创建任务
  - 执行发货
  - 失败重试
- `message_service`
  - 消息入库
  - 规则路由
  - 自动回复记录生成
- `rule_engine`
  - 规则条件匹配
- `channel_adapter`
  - 闲鱼平台接入骨架

## interfaces

对外协议层。

- `interfaces/http/routers`
  - `orders.py`
  - `messages.py`
  - `deliveries.py`
  - `events.py`

## infrastructure

基础设施实现层。

- `config`
  - 环境配置读取
- `db`
  - SQLAlchemy base、session、migrations
- `queue`
  - Celery 初始化与任务导入

## deploy

部署相关资源。

- `sql/`
  - 初始化 SQL
  - 演示种子 SQL
- `docker/`
  - API / Worker / Admin Dockerfile
- `docker-compose.yml`
  - 本地一键启动骨架

## tests

最小集成测试。

- `test_delivery_flow.py`
- `test_message_flow.py`

## 当前设计边界

当前代码结构已经适合继续往下扩展，但仍然保留了 MVP 的边界：

- 先保证订单、消息、发货三条主链路
- 暂不引入复杂多租户/权限系统
- 闲鱼真实接入保留在适配层骨架

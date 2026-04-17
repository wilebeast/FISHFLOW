CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS accounts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  platform VARCHAR(32) NOT NULL DEFAULT 'xianyu',
  nickname VARCHAR(128) NOT NULL,
  external_account_id VARCHAR(128) NOT NULL UNIQUE,
  login_status VARCHAR(32) NOT NULL DEFAULT 'active',
  health_status VARCHAR(32) NOT NULL DEFAULT 'healthy',
  credential_ref VARCHAR(256),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id UUID REFERENCES accounts(id),
  external_product_id VARCHAR(128) NOT NULL UNIQUE,
  title VARCHAR(255) NOT NULL,
  category VARCHAR(64),
  price NUMERIC(10, 2) NOT NULL DEFAULT 0,
  delivery_mode VARCHAR(32) NOT NULL DEFAULT 'auto',
  status VARCHAR(32) NOT NULL DEFAULT 'active',
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id UUID REFERENCES accounts(id),
  product_id UUID REFERENCES products(id),
  external_conversation_id VARCHAR(128) NOT NULL UNIQUE,
  buyer_id VARCHAR(128),
  current_stage VARCHAR(32) NOT NULL DEFAULT 'new_inquiry',
  handoff_status VARCHAR(32) NOT NULL DEFAULT 'bot',
  summary TEXT,
  tags JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID NOT NULL REFERENCES conversations(id),
  external_message_id VARCHAR(128) UNIQUE,
  sender_type VARCHAR(16) NOT NULL DEFAULT 'buyer',
  content_type VARCHAR(16) NOT NULL DEFAULT 'text',
  content TEXT NOT NULL,
  normalized_content TEXT NOT NULL,
  direction VARCHAR(16) NOT NULL DEFAULT 'inbound',
  processed_status VARCHAR(32) NOT NULL DEFAULT 'pending',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  inserted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS rules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(128) NOT NULL,
  scope VARCHAR(32) NOT NULL DEFAULT 'global',
  account_id UUID,
  product_id UUID,
  trigger_type VARCHAR(32) NOT NULL,
  priority INTEGER NOT NULL DEFAULT 100,
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  conditions JSONB NOT NULL DEFAULT '{}'::jsonb,
  action_type VARCHAR(32) NOT NULL,
  action_payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS templates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  template_type VARCHAR(32) NOT NULL DEFAULT 'reply',
  name VARCHAR(128) NOT NULL,
  owner_type VARCHAR(32) NOT NULL DEFAULT 'system',
  owner_id UUID,
  content TEXT NOT NULL,
  variables JSONB NOT NULL DEFAULT '{}'::jsonb,
  version INTEGER NOT NULL DEFAULT 1,
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id UUID REFERENCES accounts(id),
  product_id UUID REFERENCES products(id),
  conversation_id UUID REFERENCES conversations(id),
  external_order_id VARCHAR(128) NOT NULL UNIQUE,
  buyer_id VARCHAR(128),
  amount NUMERIC(10, 2) NOT NULL DEFAULT 0,
  currency VARCHAR(8) NOT NULL DEFAULT 'CNY',
  order_status VARCHAR(32) NOT NULL DEFAULT 'created',
  pay_status VARCHAR(32) NOT NULL DEFAULT 'unpaid',
  delivery_status VARCHAR(32) NOT NULL DEFAULT 'pending',
  paid_at TIMESTAMPTZ,
  delivered_at TIMESTAMPTZ,
  closed_at TIMESTAMPTZ,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  note TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS delivery_tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_id UUID NOT NULL REFERENCES orders(id),
  product_id UUID REFERENCES products(id),
  account_id UUID REFERENCES accounts(id),
  delivery_type VARCHAR(32) NOT NULL DEFAULT 'send_text',
  template_id UUID REFERENCES templates(id),
  payload_snapshot JSONB NOT NULL DEFAULT '{}'::jsonb,
  status VARCHAR(32) NOT NULL DEFAULT 'pending',
  attempt_count INTEGER NOT NULL DEFAULT 0,
  max_attempts INTEGER NOT NULL DEFAULT 3,
  idempotency_key VARCHAR(128) NOT NULL UNIQUE,
  result_message TEXT,
  last_error TEXT,
  next_retry_at TIMESTAMPTZ,
  executed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_accounts_external_account_id ON accounts(external_account_id);
CREATE INDEX IF NOT EXISTS ix_products_external_product_id ON products(external_product_id);
CREATE INDEX IF NOT EXISTS ix_conversations_external_conversation_id ON conversations(external_conversation_id);
CREATE INDEX IF NOT EXISTS ix_messages_conversation_id ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS ix_messages_external_message_id ON messages(external_message_id);
CREATE INDEX IF NOT EXISTS ix_messages_processed_status ON messages(processed_status);
CREATE INDEX IF NOT EXISTS ix_orders_external_order_id ON orders(external_order_id);
CREATE INDEX IF NOT EXISTS ix_orders_order_status ON orders(order_status);
CREATE INDEX IF NOT EXISTS ix_orders_pay_status ON orders(pay_status);
CREATE INDEX IF NOT EXISTS ix_orders_delivery_status ON orders(delivery_status);
CREATE INDEX IF NOT EXISTS ix_delivery_tasks_order_id ON delivery_tasks(order_id);
CREATE INDEX IF NOT EXISTS ix_delivery_tasks_status ON delivery_tasks(status);
CREATE INDEX IF NOT EXISTS ix_delivery_tasks_idempotency_key ON delivery_tasks(idempotency_key);

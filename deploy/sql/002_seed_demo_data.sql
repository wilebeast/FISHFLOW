INSERT INTO accounts (nickname, external_account_id)
VALUES ('FishFlow Demo Seller', 'acc_demo_001')
ON CONFLICT (external_account_id) DO NOTHING;

INSERT INTO products (account_id, external_product_id, title, category, price, delivery_mode)
SELECT id, 'prod_demo_001', '演示版数字商品', 'digital', 19.90, 'auto'
FROM accounts
WHERE external_account_id = 'acc_demo_001'
ON CONFLICT (external_product_id) DO NOTHING;

INSERT INTO conversations (account_id, product_id, external_conversation_id, buyer_id)
SELECT a.id, p.id, 'conv_demo_001', 'buyer_demo_001'
FROM accounts a
JOIN products p ON p.account_id = a.id
WHERE a.external_account_id = 'acc_demo_001'
ON CONFLICT (external_conversation_id) DO NOTHING;

INSERT INTO templates (template_type, name, owner_type, content, variables)
VALUES (
  'delivery',
  '默认自动发货模板',
  'system',
  '您好，您购买的内容如下：{{delivery_content}}',
  '{"delivery_content":"演示资源链接：https://example.com/download/demo"}'::jsonb
)
ON CONFLICT DO NOTHING;

INSERT INTO rules (name, scope, trigger_type, priority, enabled, conditions, action_type, action_payload)
SELECT
  '支付后默认自动发货',
  'global',
  'order_paid',
  100,
  TRUE,
  '{"event":"order_paid","require_payment_status":"paid","require_product_auto_delivery":true,"exclude_order_status":["refund_pending","refunded","closed"]}'::jsonb,
  'trigger_delivery',
  jsonb_build_object(
    'delivery_type', 'send_text',
    'template_id', t.id,
    'variables', jsonb_build_object('delivery_content', '演示资源链接：https://example.com/download/demo'),
    'max_attempts', 3
  )
FROM templates t
WHERE t.name = '默认自动发货模板'
  AND NOT EXISTS (
    SELECT 1 FROM rules WHERE name = '支付后默认自动发货'
  );

INSERT INTO orders (
  account_id,
  product_id,
  conversation_id,
  external_order_id,
  buyer_id,
  amount,
  currency,
  order_status,
  pay_status,
  delivery_status
)
SELECT
  a.id,
  p.id,
  c.id,
  'order_demo_001',
  c.buyer_id,
  19.90,
  'CNY',
  'awaiting_payment',
  'unpaid',
  'pending'
FROM accounts a
JOIN products p ON p.account_id = a.id
JOIN conversations c ON c.product_id = p.id
WHERE a.external_account_id = 'acc_demo_001'
  AND c.external_conversation_id = 'conv_demo_001'
  AND NOT EXISTS (
    SELECT 1 FROM orders WHERE external_order_id = 'order_demo_001'
  );

INSERT INTO rules (name, scope, trigger_type, priority, enabled, conditions, action_type, action_payload)
VALUES (
  '买家问候自动回复',
  'global',
  'message_received',
  90,
  TRUE,
  '{"event":"message_received","contains":"你好"}'::jsonb,
  'reply_text',
  '{"content":"您好，在的，付款后自动发货。"}'::jsonb
)
ON CONFLICT DO NOTHING;

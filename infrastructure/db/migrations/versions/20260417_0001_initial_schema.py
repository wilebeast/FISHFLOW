from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260417_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "accounts",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("platform", sa.String(length=32), nullable=False, server_default="xianyu"),
        sa.Column("nickname", sa.String(length=128), nullable=False),
        sa.Column("external_account_id", sa.String(length=128), nullable=False),
        sa.Column("login_status", sa.String(length=32), nullable=False, server_default="active"),
        sa.Column("health_status", sa.String(length=32), nullable=False, server_default="healthy"),
        sa.Column("credential_ref", sa.String(length=256), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("external_account_id"),
    )
    op.create_index("ix_accounts_external_account_id", "accounts", ["external_account_id"])

    op.create_table(
        "products",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("account_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("accounts.id")),
        sa.Column("external_product_id", sa.String(length=128), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("category", sa.String(length=64), nullable=True),
        sa.Column("price", sa.Numeric(10, 2), nullable=False, server_default="0"),
        sa.Column("delivery_mode", sa.String(length=32), nullable=False, server_default="auto"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="active"),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("external_product_id"),
    )
    op.create_index("ix_products_external_product_id", "products", ["external_product_id"])

    op.create_table(
        "conversations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("account_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("accounts.id")),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("products.id")),
        sa.Column("external_conversation_id", sa.String(length=128), nullable=False),
        sa.Column("buyer_id", sa.String(length=128), nullable=True),
        sa.Column("current_stage", sa.String(length=32), nullable=False, server_default="new_inquiry"),
        sa.Column("handoff_status", sa.String(length=32), nullable=False, server_default="bot"),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("tags", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("external_conversation_id"),
    )
    op.create_index(
        "ix_conversations_external_conversation_id",
        "conversations",
        ["external_conversation_id"],
    )

    op.create_table(
        "messages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("conversation_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("conversations.id"), nullable=False),
        sa.Column("external_message_id", sa.String(length=128), nullable=True),
        sa.Column("sender_type", sa.String(length=16), nullable=False, server_default="buyer"),
        sa.Column("content_type", sa.String(length=16), nullable=False, server_default="text"),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("normalized_content", sa.Text(), nullable=False),
        sa.Column("direction", sa.String(length=16), nullable=False, server_default="inbound"),
        sa.Column("processed_status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("inserted_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("external_message_id"),
    )
    op.create_index("ix_messages_conversation_id", "messages", ["conversation_id"])
    op.create_index("ix_messages_external_message_id", "messages", ["external_message_id"])
    op.create_index("ix_messages_processed_status", "messages", ["processed_status"])

    op.create_table(
        "rules",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("scope", sa.String(length=32), nullable=False, server_default="global"),
        sa.Column("account_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("trigger_type", sa.String(length=32), nullable=False),
        sa.Column("priority", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("conditions", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("action_type", sa.String(length=32), nullable=False),
        sa.Column("action_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_rules_scope", "rules", ["scope"])
    op.create_index("ix_rules_account_id", "rules", ["account_id"])
    op.create_index("ix_rules_product_id", "rules", ["product_id"])
    op.create_index("ix_rules_priority", "rules", ["priority"])
    op.create_index("ix_rules_enabled", "rules", ["enabled"])

    op.create_table(
        "templates",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("template_type", sa.String(length=32), nullable=False, server_default="reply"),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("owner_type", sa.String(length=32), nullable=False, server_default="system"),
        sa.Column("owner_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("variables", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_templates_template_type", "templates", ["template_type"])
    op.create_index("ix_templates_owner_type", "templates", ["owner_type"])
    op.create_index("ix_templates_enabled", "templates", ["enabled"])

    op.create_table(
        "orders",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("account_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("accounts.id")),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("products.id")),
        sa.Column("conversation_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("conversations.id")),
        sa.Column("external_order_id", sa.String(length=128), nullable=False),
        sa.Column("buyer_id", sa.String(length=128), nullable=True),
        sa.Column("amount", sa.Numeric(10, 2), nullable=False, server_default="0"),
        sa.Column("currency", sa.String(length=8), nullable=False, server_default="CNY"),
        sa.Column("order_status", sa.String(length=32), nullable=False, server_default="created"),
        sa.Column("pay_status", sa.String(length=32), nullable=False, server_default="unpaid"),
        sa.Column("delivery_status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("paid_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("delivered_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("external_order_id"),
    )
    op.create_index("ix_orders_external_order_id", "orders", ["external_order_id"])
    op.create_index("ix_orders_order_status", "orders", ["order_status"])
    op.create_index("ix_orders_pay_status", "orders", ["pay_status"])
    op.create_index("ix_orders_delivery_status", "orders", ["delivery_status"])

    op.create_table(
        "delivery_tasks",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("order_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("orders.id"), nullable=False),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("products.id")),
        sa.Column("account_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("accounts.id")),
        sa.Column("delivery_type", sa.String(length=32), nullable=False, server_default="send_text"),
        sa.Column("template_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("templates.id")),
        sa.Column("payload_snapshot", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="pending"),
        sa.Column("attempt_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("max_attempts", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("idempotency_key", sa.String(length=128), nullable=False),
        sa.Column("result_message", sa.Text(), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("next_retry_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("executed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("idempotency_key"),
    )
    op.create_index("ix_delivery_tasks_order_id", "delivery_tasks", ["order_id"])
    op.create_index("ix_delivery_tasks_status", "delivery_tasks", ["status"])
    op.create_index("ix_delivery_tasks_idempotency_key", "delivery_tasks", ["idempotency_key"])


def downgrade() -> None:
    op.drop_index("ix_delivery_tasks_idempotency_key", table_name="delivery_tasks")
    op.drop_index("ix_delivery_tasks_status", table_name="delivery_tasks")
    op.drop_index("ix_delivery_tasks_order_id", table_name="delivery_tasks")
    op.drop_table("delivery_tasks")
    op.drop_index("ix_orders_delivery_status", table_name="orders")
    op.drop_index("ix_orders_pay_status", table_name="orders")
    op.drop_index("ix_orders_order_status", table_name="orders")
    op.drop_index("ix_orders_external_order_id", table_name="orders")
    op.drop_table("orders")
    op.drop_index("ix_templates_enabled", table_name="templates")
    op.drop_index("ix_templates_owner_type", table_name="templates")
    op.drop_index("ix_templates_template_type", table_name="templates")
    op.drop_table("templates")
    op.drop_index("ix_rules_enabled", table_name="rules")
    op.drop_index("ix_rules_priority", table_name="rules")
    op.drop_index("ix_rules_product_id", table_name="rules")
    op.drop_index("ix_rules_account_id", table_name="rules")
    op.drop_index("ix_rules_scope", table_name="rules")
    op.drop_table("rules")
    op.drop_index("ix_messages_processed_status", table_name="messages")
    op.drop_index("ix_messages_external_message_id", table_name="messages")
    op.drop_index("ix_messages_conversation_id", table_name="messages")
    op.drop_table("messages")
    op.drop_index("ix_conversations_external_conversation_id", table_name="conversations")
    op.drop_table("conversations")
    op.drop_index("ix_products_external_product_id", table_name="products")
    op.drop_table("products")
    op.drop_index("ix_accounts_external_account_id", table_name="accounts")
    op.drop_table("accounts")

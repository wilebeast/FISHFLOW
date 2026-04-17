from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260418_0003"
down_revision = "20260418_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("accounts", sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("accounts", sa.Column("last_check_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("accounts", sa.Column("risk_level", sa.String(length=32), nullable=False, server_default="low"))
    op.add_column("accounts", sa.Column("disabled_reason", sa.String(length=255), nullable=True))

    op.create_table(
        "inventory_items",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("resource_type", sa.String(length=32), nullable=False),
        sa.Column("product_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("code", sa.String(length=255), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="available"),
        sa.Column("allocated_order_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("note", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"]),
        sa.ForeignKeyConstraint(["allocated_order_id"], ["orders.id"]),
    )
    op.create_index("ix_inventory_items_resource_type", "inventory_items", ["resource_type"])
    op.create_index("ix_inventory_items_status", "inventory_items", ["status"])

    op.create_table(
        "notification_configs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("channel", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("target", sa.Text(), nullable=True),
        sa.Column("config_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_notification_configs_channel", "notification_configs", ["channel"])

    op.create_table(
        "ai_reply_configs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(length=128), nullable=False, server_default="default"),
        sa.Column("provider", sa.String(length=64), nullable=False, server_default="openai-compatible"),
        sa.Column("model", sa.String(length=128), nullable=False, server_default="gpt-5-mini"),
        sa.Column("system_prompt", sa.Text(), nullable=False, server_default="You are a concise sales assistant."),
        sa.Column("temperature", sa.Float(), nullable=False, server_default="0.2"),
        sa.Column("max_tokens", sa.Integer(), nullable=False, server_default="200"),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("guardrails_json", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "ai_call_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("scene", sa.String(length=64), nullable=False),
        sa.Column("model", sa.String(length=128), nullable=False),
        sa.Column("input_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("output_tokens", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("latency_ms", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="success"),
        sa.Column("request_snapshot", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("response_snapshot", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_ai_call_logs_scene", "ai_call_logs", ["scene"])


def downgrade() -> None:
    op.drop_index("ix_ai_call_logs_scene", table_name="ai_call_logs")
    op.drop_table("ai_call_logs")
    op.drop_table("ai_reply_configs")

    op.drop_index("ix_notification_configs_channel", table_name="notification_configs")
    op.drop_table("notification_configs")

    op.drop_index("ix_inventory_items_status", table_name="inventory_items")
    op.drop_index("ix_inventory_items_resource_type", table_name="inventory_items")
    op.drop_table("inventory_items")

    op.drop_column("accounts", "disabled_reason")
    op.drop_column("accounts", "risk_level")
    op.drop_column("accounts", "last_check_at")
    op.drop_column("accounts", "last_login_at")

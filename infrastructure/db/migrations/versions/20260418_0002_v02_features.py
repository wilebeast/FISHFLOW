from __future__ import annotations

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "20260418_0002"
down_revision = "20260417_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("products", sa.Column("delivery_template_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("products", sa.Column("faq_template_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("products", sa.Column("rule_profile_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column(
        "products",
        sa.Column("auto_delivery_enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_foreign_key(None, "products", "templates", ["delivery_template_id"], ["id"])
    op.create_foreign_key(None, "products", "templates", ["faq_template_id"], ["id"])

    op.add_column("conversations", sa.Column("last_message_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("conversations", sa.Column("assigned_to", sa.String(length=128), nullable=True))
    op.add_column(
        "conversations",
        sa.Column("priority", sa.String(length=32), nullable=False, server_default="normal"),
    )
    op.add_column(
        "conversations",
        sa.Column("unread_count", sa.Integer(), nullable=False, server_default="0"),
    )

    op.add_column("messages", sa.Column("reply_to_message_id", postgresql.UUID(as_uuid=True), nullable=True))
    op.add_column("messages", sa.Column("send_status", sa.String(length=32), nullable=True))
    op.add_column("messages", sa.Column("send_error", sa.Text(), nullable=True))
    op.add_column("messages", sa.Column("trace_id", sa.String(length=128), nullable=True))

    op.add_column("templates", sa.Column("description", sa.Text(), nullable=True))
    op.add_column("templates", sa.Column("category", sa.String(length=64), nullable=True))
    op.add_column(
        "templates",
        sa.Column("is_default", sa.Boolean(), nullable=False, server_default=sa.false()),
    )

    op.create_table(
        "system_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("severity", sa.String(length=16), nullable=False, server_default="info"),
        sa.Column("source", sa.String(length=64), nullable=False),
        sa.Column("details", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_system_events_event_type", "system_events", ["event_type"])
    op.create_index("ix_system_events_severity", "system_events", ["severity"])
    op.create_index("ix_system_events_source", "system_events", ["source"])

    op.create_table(
        "admin_actions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("actor", sa.String(length=128), nullable=False, server_default="system"),
        sa.Column("action", sa.String(length=64), nullable=False),
        sa.Column("target_type", sa.String(length=64), nullable=False),
        sa.Column("target_id", sa.String(length=128), nullable=False),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_admin_actions_action", "admin_actions", ["action"])
    op.create_index("ix_admin_actions_target_type", "admin_actions", ["target_type"])
    op.create_index("ix_admin_actions_target_id", "admin_actions", ["target_id"])


def downgrade() -> None:
    op.drop_index("ix_admin_actions_target_id", table_name="admin_actions")
    op.drop_index("ix_admin_actions_target_type", table_name="admin_actions")
    op.drop_index("ix_admin_actions_action", table_name="admin_actions")
    op.drop_table("admin_actions")

    op.drop_index("ix_system_events_source", table_name="system_events")
    op.drop_index("ix_system_events_severity", table_name="system_events")
    op.drop_index("ix_system_events_event_type", table_name="system_events")
    op.drop_table("system_events")

    op.drop_column("templates", "is_default")
    op.drop_column("templates", "category")
    op.drop_column("templates", "description")

    op.drop_column("messages", "trace_id")
    op.drop_column("messages", "send_error")
    op.drop_column("messages", "send_status")
    op.drop_column("messages", "reply_to_message_id")

    op.drop_column("conversations", "unread_count")
    op.drop_column("conversations", "priority")
    op.drop_column("conversations", "assigned_to")
    op.drop_column("conversations", "last_message_at")

    op.drop_constraint(None, "products", type_="foreignkey")
    op.drop_constraint(None, "products", type_="foreignkey")
    op.drop_column("products", "auto_delivery_enabled")
    op.drop_column("products", "rule_profile_id")
    op.drop_column("products", "faq_template_id")
    op.drop_column("products", "delivery_template_id")

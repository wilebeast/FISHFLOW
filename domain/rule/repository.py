from __future__ import annotations

from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from domain.rule.models import Rule


class RuleRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _coerce_uuid(value: UUID | str) -> UUID:
        return value if isinstance(value, UUID) else UUID(str(value))

    def get(self, rule_id: UUID | str) -> Rule | None:
        stmt = select(Rule).where(Rule.id == self._coerce_uuid(rule_id))
        return self.session.scalar(stmt)

    def list_enabled(self, trigger_type: str) -> list[Rule]:
        stmt = (
            select(Rule)
            .where(Rule.enabled.is_(True), Rule.trigger_type == trigger_type)
            .order_by(desc(Rule.priority))
        )
        return list(self.session.scalars(stmt).all())

    def list_recent(
        self,
        scope: str | None = None,
        trigger_type: str | None = None,
        enabled: bool | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Rule]:
        stmt = select(Rule)
        if scope:
            stmt = stmt.where(Rule.scope == scope)
        if trigger_type:
            stmt = stmt.where(Rule.trigger_type == trigger_type)
        if enabled is not None:
            stmt = stmt.where(Rule.enabled.is_(enabled))
        stmt = stmt.order_by(desc(Rule.priority), desc(Rule.updated_at)).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

    def save(self, rule: Rule) -> Rule:
        self.session.add(rule)
        self.session.flush()
        return rule

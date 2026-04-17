from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from domain.rule.models import Rule


class RuleRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_enabled(self, trigger_type: str) -> list[Rule]:
        stmt = (
            select(Rule)
            .where(Rule.enabled.is_(True), Rule.trigger_type == trigger_type)
            .order_by(desc(Rule.priority))
        )
        return list(self.session.scalars(stmt).all())

    def save(self, rule: Rule) -> Rule:
        self.session.add(rule)
        self.session.flush()
        return rule

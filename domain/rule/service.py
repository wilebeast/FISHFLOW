from __future__ import annotations

from domain.rule.models import Rule
from domain.rule.repository import RuleRepository
from domain.rule.schemas import RuleUpdate


class RuleService:
    def __init__(self, repository: RuleRepository) -> None:
        self.repository = repository

    def list_candidates(self, trigger_type: str) -> list[Rule]:
        return self.repository.list_enabled(trigger_type)

    @staticmethod
    def apply_update(rule: Rule, payload: RuleUpdate) -> Rule:
        for field, value in payload.model_dump(exclude_unset=True).items():
            if hasattr(value, "value"):
                setattr(rule, field, value.value)
            else:
                setattr(rule, field, value)
        return rule

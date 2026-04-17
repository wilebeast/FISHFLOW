from __future__ import annotations

from domain.rule.models import Rule
from domain.rule.repository import RuleRepository


class RuleService:
    def __init__(self, repository: RuleRepository) -> None:
        self.repository = repository

    def list_candidates(self, trigger_type: str) -> list[Rule]:
        return self.repository.list_enabled(trigger_type)

from __future__ import annotations

from dataclasses import dataclass

from domain.rule.enums import ActionType, TriggerType
from domain.rule.models import Rule
from domain.rule.repository import RuleRepository
from services.rule_engine.engine import RuleEngine


@dataclass(slots=True)
class MessageRouteResult:
    action_type: str
    action_payload: dict
    matched_rule_id: str | None = None


class MessageRouter:
    def __init__(self, rule_repository: RuleRepository) -> None:
        self.rule_repository = rule_repository
        self.rule_engine = RuleEngine()

    def route(self, message_context: dict) -> MessageRouteResult:
        rules = self.rule_repository.list_enabled(TriggerType.MESSAGE_RECEIVED.value)
        matched_rule = self.rule_engine.match(rules, message_context)
        if matched_rule:
            return self._from_rule(matched_rule)
        return MessageRouteResult(
            action_type=ActionType.REPLY_AI.value,
            action_payload={"reason": "no_rule_matched"},
        )

    @staticmethod
    def _from_rule(rule: Rule) -> MessageRouteResult:
        return MessageRouteResult(
            action_type=rule.action_type,
            action_payload=rule.action_payload,
            matched_rule_id=str(rule.id),
        )

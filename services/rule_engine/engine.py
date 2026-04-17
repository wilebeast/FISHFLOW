from __future__ import annotations

from domain.rule.models import Rule


class RuleEngine:
    def match(self, rules: list[Rule], context: dict) -> Rule | None:
        for rule in rules:
            if self._matches(rule.conditions, context):
                return rule
        return None

    def _matches(self, conditions: dict, context: dict) -> bool:
        event = conditions.get("event")
        if event and context.get("event") != event:
            return False
        contains = conditions.get("contains")
        if contains and contains not in context.get("normalized_content", ""):
            return False
        require_payment_status = conditions.get("require_payment_status")
        if require_payment_status and context.get("pay_status") != require_payment_status:
            return False
        require_auto_delivery = conditions.get("require_product_auto_delivery")
        if require_auto_delivery and not context.get("product_auto_delivery"):
            return False
        exclude_statuses = set(conditions.get("exclude_order_status", []))
        if context.get("order_status") in exclude_statuses:
            return False
        return True

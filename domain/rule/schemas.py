from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from domain.rule.enums import ActionType, RuleScope, TriggerType


class RuleCreate(BaseModel):
    name: str
    scope: RuleScope = RuleScope.GLOBAL
    account_id: UUID | None = None
    product_id: UUID | None = None
    trigger_type: TriggerType
    priority: int = 100
    enabled: bool = True
    conditions: dict = {}
    action_type: ActionType
    action_payload: dict = {}


class RuleUpdate(BaseModel):
    name: str | None = None
    scope: RuleScope | None = None
    account_id: UUID | None = None
    product_id: UUID | None = None
    trigger_type: TriggerType | None = None
    priority: int | None = None
    enabled: bool | None = None
    conditions: dict | None = None
    action_type: ActionType | None = None
    action_payload: dict | None = None


class RuleRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    scope: RuleScope
    account_id: UUID | None = None
    product_id: UUID | None = None
    trigger_type: TriggerType
    priority: int
    enabled: bool
    conditions: dict
    action_type: ActionType
    action_payload: dict

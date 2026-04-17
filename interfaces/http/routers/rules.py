from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from domain.rule.models import Rule
from domain.rule.repository import RuleRepository
from domain.rule.schemas import RuleCreate, RuleRead, RuleUpdate
from domain.rule.service import RuleService
from infrastructure.db.session import get_db
from interfaces.http.routers.dto.common import ActionAccepted
from services.audit_service.logger import AuditLogger

router = APIRouter()


@router.get("", response_model=list[RuleRead])
def list_rules(
    scope: str | None = Query(default=None),
    trigger_type: str | None = Query(default=None),
    enabled: bool | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[Rule]:
    return RuleRepository(db).list_recent(
        scope=scope,
        trigger_type=trigger_type,
        enabled=enabled,
        limit=limit,
        offset=offset,
    )


@router.post("", response_model=RuleRead)
def create_rule(payload: RuleCreate, db: Session = Depends(get_db)) -> Rule:
    rule = Rule(
        **{
            **payload.model_dump(),
            "scope": payload.scope.value,
            "trigger_type": payload.trigger_type.value,
            "action_type": payload.action_type.value,
        }
    )
    RuleRepository(db).save(rule)
    AuditLogger(db).log("create_rule", "rule", str(rule.id), payload.model_dump())
    db.commit()
    db.refresh(rule)
    return rule


@router.get("/{rule_id}", response_model=RuleRead)
def get_rule(rule_id: str, db: Session = Depends(get_db)) -> Rule:
    rule = RuleRepository(db).get(rule_id)
    if rule is None:
        raise HTTPException(status_code=404, detail="rule not found")
    return rule


@router.patch("/{rule_id}", response_model=RuleRead)
def update_rule(rule_id: str, payload: RuleUpdate, db: Session = Depends(get_db)) -> Rule:
    repository = RuleRepository(db)
    rule = repository.get(rule_id)
    if rule is None:
        raise HTTPException(status_code=404, detail="rule not found")
    RuleService.apply_update(rule, payload)
    AuditLogger(db).log("update_rule", "rule", str(rule.id), payload.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(rule)
    return rule


@router.post("/{rule_id}/enable", response_model=ActionAccepted)
def enable_rule(rule_id: str, db: Session = Depends(get_db)) -> ActionAccepted:
    repository = RuleRepository(db)
    rule = repository.get(rule_id)
    if rule is None:
        raise HTTPException(status_code=404, detail="rule not found")
    rule.enabled = True
    AuditLogger(db).log("enable_rule", "rule", str(rule.id), {})
    db.commit()
    return ActionAccepted(status="ok", detail="rule enabled")


@router.post("/{rule_id}/disable", response_model=ActionAccepted)
def disable_rule(rule_id: str, db: Session = Depends(get_db)) -> ActionAccepted:
    repository = RuleRepository(db)
    rule = repository.get(rule_id)
    if rule is None:
        raise HTTPException(status_code=404, detail="rule not found")
    rule.enabled = False
    AuditLogger(db).log("disable_rule", "rule", str(rule.id), {})
    db.commit()
    return ActionAccepted(status="ok", detail="rule disabled")

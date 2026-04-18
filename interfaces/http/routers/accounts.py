from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from apps.worker.tasks_sync import sync_orders, sync_products
from domain.account.models import Account
from domain.account.repository import AccountRepository
from domain.account.schemas import AccountCreate, AccountRead, AccountUpdate, DisableAccountPayload
from domain.account.service import AccountService
from infrastructure.db.session import get_db
from interfaces.http.routers.dto.common import ActionAccepted
from services.audit_service.logger import AuditLogger


router = APIRouter()


@router.get("", response_model=list[AccountRead])
def list_accounts(
    q: str | None = Query(default=None),
    login_status: str | None = Query(default=None),
    health_status: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[Account]:
    return AccountRepository(db).list_recent(
        q=q,
        login_status=login_status,
        health_status=health_status,
        limit=limit,
        offset=offset,
    )


@router.post("", response_model=AccountRead)
def create_account(payload: AccountCreate, db: Session = Depends(get_db)) -> Account:
    repository = AccountRepository(db)
    existing = repository.get_by_external_account_id(payload.external_account_id)
    if existing:
        return existing
    account = Account(**payload.model_dump())
    repository.save(account)
    AuditLogger(db).log("create_account", "account", str(account.id), payload.model_dump())
    db.commit()
    db.refresh(account)
    return account


@router.get("/{account_id}", response_model=AccountRead)
def get_account(account_id: str, db: Session = Depends(get_db)) -> Account:
    account = AccountRepository(db).get(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="account not found")
    return account


@router.patch("/{account_id}", response_model=AccountRead)
def update_account(account_id: str, payload: AccountUpdate, db: Session = Depends(get_db)) -> Account:
    repository = AccountRepository(db)
    account = repository.get(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="account not found")
    AccountService.apply_update(account, payload)
    AuditLogger(db).log("update_account", "account", str(account.id), payload.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(account)
    return account


@router.post("/{account_id}/health-check", response_model=ActionAccepted)
def account_health_check(account_id: str, db: Session = Depends(get_db)) -> ActionAccepted:
    repository = AccountRepository(db)
    account = repository.get(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="account not found")
    AccountService.run_health_check(account)
    AuditLogger(db).log("account_health_check", "account", str(account.id), {"health_status": account.health_status})
    db.commit()
    return ActionAccepted(status="ok", detail=f"health_status={account.health_status}")


@router.post("/{account_id}/disable", response_model=ActionAccepted)
def disable_account(account_id: str, payload: DisableAccountPayload, db: Session = Depends(get_db)) -> ActionAccepted:
    repository = AccountRepository(db)
    account = repository.get(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="account not found")
    account.login_status = "disabled"
    account.health_status = "error"
    account.disabled_reason = payload.reason
    AuditLogger(db).log("disable_account", "account", str(account.id), payload.model_dump())
    db.commit()
    return ActionAccepted(status="ok", detail="account disabled")


@router.post("/{account_id}/sync-products", response_model=ActionAccepted)
def sync_account_products(account_id: str, db: Session = Depends(get_db)) -> ActionAccepted:
    account = AccountRepository(db).get(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="account not found")
    sync_products.delay(str(account.id))
    AuditLogger(db).log("sync_products", "account", str(account.id), {})
    db.commit()
    return ActionAccepted(status="ok", detail="product sync queued")


@router.post("/{account_id}/sync-orders", response_model=ActionAccepted)
def sync_account_orders(account_id: str, db: Session = Depends(get_db)) -> ActionAccepted:
    account = AccountRepository(db).get(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="account not found")
    sync_orders.delay(str(account.id))
    AuditLogger(db).log("sync_orders", "account", str(account.id), {})
    db.commit()
    return ActionAccepted(status="ok", detail="order sync queued")

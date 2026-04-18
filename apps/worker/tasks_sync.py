from __future__ import annotations

from apps.worker.celery_app import celery_app
from domain.account.repository import AccountRepository
from infrastructure.db.session import SessionLocal
from services.channel_adapter.xianyu.sync_service import XianyuSyncService


@celery_app.task(name="xianyu.sync_products")
def sync_products(account_id: str) -> int:
    session = SessionLocal()
    try:
        account = AccountRepository(session).get(account_id)
        if account is None:
            raise ValueError(f"account not found: {account_id}")
        synced = XianyuSyncService(session).sync_products(account)
        session.commit()
        return synced
    finally:
        session.close()


@celery_app.task(name="xianyu.sync_orders")
def sync_orders(account_id: str) -> int:
    session = SessionLocal()
    try:
        account = AccountRepository(session).get(account_id)
        if account is None:
            raise ValueError(f"account not found: {account_id}")
        synced = XianyuSyncService(session).sync_orders(account)
        session.commit()
        return synced
    finally:
        session.close()

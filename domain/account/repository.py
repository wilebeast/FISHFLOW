from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from domain.account.models import Account


class AccountRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _coerce_uuid(value: UUID | str) -> UUID:
        return value if isinstance(value, UUID) else UUID(str(value))

    def get(self, account_id: UUID | str) -> Account | None:
        stmt = select(Account).where(Account.id == self._coerce_uuid(account_id))
        return self.session.scalar(stmt)

    def get_by_external_account_id(self, external_account_id: str) -> Account | None:
        stmt = select(Account).where(Account.external_account_id == external_account_id)
        return self.session.scalar(stmt)

    def list_recent(
        self,
        q: str | None = None,
        login_status: str | None = None,
        health_status: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Account]:
        stmt = select(Account)
        if q:
            stmt = stmt.where(
                Account.nickname.ilike(f"%{q}%") | Account.external_account_id.ilike(f"%{q}%")
            )
        if login_status:
            stmt = stmt.where(Account.login_status == login_status)
        if health_status:
            stmt = stmt.where(Account.health_status == health_status)
        stmt = stmt.order_by(desc(Account.updated_at)).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

    def touch_checked(self, account: Account) -> Account:
        account.last_check_at = datetime.now(timezone.utc)
        return account

    def save(self, account: Account) -> Account:
        self.session.add(account)
        self.session.flush()
        return account

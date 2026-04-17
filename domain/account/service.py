from __future__ import annotations

from datetime import datetime, timezone

from domain.account.models import Account
from domain.account.schemas import AccountUpdate


class AccountService:
    @staticmethod
    def apply_update(account: Account, payload: AccountUpdate) -> Account:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(account, field, value)
        return account

    @staticmethod
    def run_health_check(account: Account) -> Account:
        account.last_check_at = datetime.now(timezone.utc)
        if account.login_status == "disabled":
            account.health_status = "error"
        elif account.login_status in {"expired", "risk"}:
            account.health_status = "warning"
        else:
            account.health_status = "healthy"
        return account

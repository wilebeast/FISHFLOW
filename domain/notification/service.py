from __future__ import annotations

from domain.notification.models import NotificationConfig
from domain.notification.schemas import NotificationConfigUpdate


class NotificationConfigService:
    @staticmethod
    def apply_update(config: NotificationConfig, payload: NotificationConfigUpdate) -> NotificationConfig:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(config, field, value)
        return config

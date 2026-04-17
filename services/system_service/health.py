from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.orm import Session

from domain.system_event.repository import SystemEventRepository


class SystemHealthService:
    def __init__(self, session: Session, redis_url: str) -> None:
        self.session = session
        self.redis_url = redis_url
        self.events = SystemEventRepository(session)

    def get_health(self) -> dict:
        database_ok = True
        try:
            self.session.execute(text("select 1"))
        except Exception:
            database_ok = False

        redis_ok = True
        try:
            from redis import Redis

            Redis.from_url(self.redis_url).ping()
        except Exception:
            redis_ok = False

        return {
            "api": "ok",
            "database": "ok" if database_ok else "error",
            "redis": "ok" if redis_ok else "error",
            "worker": "unknown",
        }

    def get_queue(self) -> dict:
        queue_info = {"broker": self.redis_url, "worker": "unknown", "queued_tasks": None}
        try:
            from celery import current_app

            inspect = current_app.control.inspect()
            stats = inspect.stats()
            queue_info["worker"] = "online" if stats else "offline"
        except Exception:
            queue_info["worker"] = "offline"
        return queue_info

    def get_recent_errors(self) -> list:
        return self.events.list_recent(limit=20)

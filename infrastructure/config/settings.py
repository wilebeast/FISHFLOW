from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    env: str = "development"
    debug: bool = True
    database_url: str = "postgresql+psycopg://fishflow:fishflow@localhost:5432/fishflow"
    redis_url: str = "redis://localhost:6379/0"
    celery_broker_url: str = "redis://localhost:6379/2"
    celery_result_backend: str = "redis://localhost:6379/2"
    api_title: str = "FishFlow API"
    api_version: str = "0.1.0"
    xianyu_api_base_url: str = "https://api.xianyu.com"
    xianyu_bridge_api_base_url: str = "http://127.0.0.1:8787"
    xianyu_bridge_token: str | None = None
    xianyu_timeout_seconds: int = 15

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"1", "true", "yes", "on", "debug"}:
                return True
            if normalized in {"0", "false", "no", "off", "release", "production"}:
                return False
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()

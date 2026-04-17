from functools import lru_cache

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


@lru_cache
def get_settings() -> Settings:
    return Settings()

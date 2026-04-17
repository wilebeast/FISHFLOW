from celery import Celery

from infrastructure.config.settings import get_settings


settings = get_settings()

celery_app = Celery(
    "fishflow",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.imports = (
    "apps.worker.tasks_order",
    "apps.worker.tasks_delivery",
    "apps.worker.tasks_message",
)

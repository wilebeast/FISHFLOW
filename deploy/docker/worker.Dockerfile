FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
COPY apps /app/apps
COPY domain /app/domain
COPY infrastructure /app/infrastructure
COPY interfaces /app/interfaces
COPY services /app/services
COPY scripts /app/scripts
COPY alembic.ini /app/alembic.ini

RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -e .

CMD ["celery", "-A", "apps.worker.celery_app.celery_app", "worker", "-l", "info"]

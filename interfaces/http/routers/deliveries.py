from __future__ import annotations

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from apps.worker.tasks_delivery import retry_task
from domain.delivery.repository import DeliveryTaskRepository
from domain.delivery.schemas import DeliveryTaskRead
from infrastructure.db.session import get_db
from interfaces.http.routers.dto.common import ActionAccepted


router = APIRouter()


@router.get("", response_model=list[DeliveryTaskRead])
def list_delivery_tasks(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[DeliveryTaskRead]:
    repository = DeliveryTaskRepository(db)
    return repository.list_recent(limit=limit, offset=offset)


@router.get("/{task_id}", response_model=DeliveryTaskRead)
def get_delivery_task(task_id: str, db: Session = Depends(get_db)) -> DeliveryTaskRead:
    repository = DeliveryTaskRepository(db)
    task = repository.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="delivery task not found")
    return task


@router.post("/{task_id}/retry", response_model=ActionAccepted)
def retry_delivery_task(
    task_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> ActionAccepted:
    repository = DeliveryTaskRepository(db)
    task = repository.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="delivery task not found")
    if task.status == "success":
        raise HTTPException(status_code=400, detail="successful task does not need retry")
    background_tasks.add_task(retry_task.delay, task_id)
    return ActionAccepted(status="accepted", detail=f"retry queued for task {task_id}")

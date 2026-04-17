from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from domain.inventory.models import InventoryItem
from domain.inventory.repository import InventoryRepository
from domain.inventory.schemas import InventoryAllocatePayload, InventoryCreate, InventoryRead, InventoryUpdate
from domain.inventory.service import InventoryService
from infrastructure.db.session import get_db
from interfaces.http.routers.dto.common import ActionAccepted
from services.audit_service.logger import AuditLogger


router = APIRouter()


@router.get("", response_model=list[InventoryRead])
def list_inventory(
    resource_type: str | None = Query(default=None),
    status: str | None = Query(default=None),
    product_id: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[InventoryItem]:
    return InventoryRepository(db).list_recent(
        resource_type=resource_type,
        status=status,
        product_id=product_id,
        limit=limit,
        offset=offset,
    )


@router.post("", response_model=InventoryRead)
def create_inventory_item(payload: InventoryCreate, db: Session = Depends(get_db)) -> InventoryItem:
    item = InventoryItem(**payload.model_dump())
    InventoryRepository(db).save(item)
    AuditLogger(db).log("create_inventory_item", "inventory", str(item.id), payload.model_dump())
    db.commit()
    db.refresh(item)
    return item


@router.get("/{item_id}", response_model=InventoryRead)
def get_inventory_item(item_id: str, db: Session = Depends(get_db)) -> InventoryItem:
    item = InventoryRepository(db).get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="inventory item not found")
    return item


@router.patch("/{item_id}", response_model=InventoryRead)
def update_inventory_item(item_id: str, payload: InventoryUpdate, db: Session = Depends(get_db)) -> InventoryItem:
    repository = InventoryRepository(db)
    item = repository.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="inventory item not found")
    InventoryService.apply_update(item, payload)
    AuditLogger(db).log("update_inventory_item", "inventory", str(item.id), payload.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(item)
    return item


@router.post("/{item_id}/allocate", response_model=ActionAccepted)
def allocate_inventory_item(item_id: str, payload: InventoryAllocatePayload, db: Session = Depends(get_db)) -> ActionAccepted:
    repository = InventoryRepository(db)
    item = repository.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="inventory item not found")
    item.status = "allocated"
    item.allocated_order_id = payload.order_id
    AuditLogger(db).log("allocate_inventory_item", "inventory", str(item.id), payload.model_dump())
    db.commit()
    return ActionAccepted(status="ok", detail="inventory allocated")


@router.post("/{item_id}/disable", response_model=ActionAccepted)
def disable_inventory_item(item_id: str, db: Session = Depends(get_db)) -> ActionAccepted:
    repository = InventoryRepository(db)
    item = repository.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="inventory item not found")
    item.status = "disabled"
    AuditLogger(db).log("disable_inventory_item", "inventory", str(item.id), {})
    db.commit()
    return ActionAccepted(status="ok", detail="inventory disabled")

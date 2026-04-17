from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from domain.product.models import Product
from domain.product.repository import ProductRepository
from domain.product.schemas import ProductCreate, ProductRead, ProductUpdate
from domain.product.service import ProductService
from infrastructure.db.session import get_db
from interfaces.http.routers.dto.common import ActionAccepted
from services.audit_service.logger import AuditLogger


router = APIRouter()


class BindReference(BaseModel):
    id: UUID


@router.get("", response_model=list[ProductRead])
def list_products(
    q: str | None = Query(default=None),
    status: str | None = Query(default=None),
    delivery_mode: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[Product]:
    return ProductRepository(db).list_recent(
        q=q,
        status=status,
        delivery_mode=delivery_mode,
        limit=limit,
        offset=offset,
    )


@router.post("", response_model=ProductRead)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)) -> Product:
    repository = ProductRepository(db)
    existing = repository.get_by_external_product_id(payload.external_product_id)
    if existing:
        return existing

    product = Product(**payload.model_dump())
    repository.save(product)
    AuditLogger(db).log("create_product", "product", str(product.id), payload.model_dump())
    db.commit()
    db.refresh(product)
    return product


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: str, db: Session = Depends(get_db)) -> Product:
    product = ProductRepository(db).get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="product not found")
    return product


@router.patch("/{product_id}", response_model=ProductRead)
def update_product(product_id: str, payload: ProductUpdate, db: Session = Depends(get_db)) -> Product:
    repository = ProductRepository(db)
    product = repository.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="product not found")

    ProductService().apply_update(product, payload)
    AuditLogger(db).log("update_product", "product", str(product.id), payload.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(product)
    return product


@router.post("/{product_id}/bind-rule", response_model=ActionAccepted)
def bind_rule(product_id: str, payload: BindReference, db: Session = Depends(get_db)) -> ActionAccepted:
    repository = ProductRepository(db)
    product = repository.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="product not found")
    product.rule_profile_id = payload.id
    AuditLogger(db).log("bind_rule", "product", str(product.id), {"rule_profile_id": payload.id})
    db.commit()
    return ActionAccepted(status="ok", detail="rule bound")


@router.post("/{product_id}/bind-delivery-template", response_model=ActionAccepted)
def bind_delivery_template(product_id: str, payload: BindReference, db: Session = Depends(get_db)) -> ActionAccepted:
    repository = ProductRepository(db)
    product = repository.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="product not found")
    product.delivery_template_id = payload.id
    AuditLogger(db).log("bind_delivery_template", "product", str(product.id), {"delivery_template_id": payload.id})
    db.commit()
    return ActionAccepted(status="ok", detail="delivery template bound")


@router.post("/{product_id}/bind-faq-template", response_model=ActionAccepted)
def bind_faq_template(product_id: str, payload: BindReference, db: Session = Depends(get_db)) -> ActionAccepted:
    repository = ProductRepository(db)
    product = repository.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="product not found")
    product.faq_template_id = payload.id
    AuditLogger(db).log("bind_faq_template", "product", str(product.id), {"faq_template_id": payload.id})
    db.commit()
    return ActionAccepted(status="ok", detail="faq template bound")


@router.post("/{product_id}/toggle-auto-delivery", response_model=ActionAccepted)
def toggle_auto_delivery(product_id: str, db: Session = Depends(get_db)) -> ActionAccepted:
    repository = ProductRepository(db)
    product = repository.get(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="product not found")
    product.auto_delivery_enabled = not product.auto_delivery_enabled
    AuditLogger(db).log(
        "toggle_auto_delivery",
        "product",
        str(product.id),
        {"auto_delivery_enabled": product.auto_delivery_enabled},
    )
    db.commit()
    return ActionAccepted(status="ok", detail=f"auto_delivery_enabled={product.auto_delivery_enabled}")

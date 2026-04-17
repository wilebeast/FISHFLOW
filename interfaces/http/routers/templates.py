from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from domain.template.models import Template
from domain.template.repository import TemplateRepository
from domain.template.schemas import TemplateCreate, TemplateRead, TemplateUpdate
from domain.template.service import TemplateService
from infrastructure.db.session import get_db
from services.audit_service.logger import AuditLogger

router = APIRouter()


@router.get("", response_model=list[TemplateRead])
def list_templates(
    template_type: str | None = Query(default=None),
    enabled: bool | None = Query(default=None),
    q: str | None = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[Template]:
    return TemplateRepository(db).list_recent(
        template_type=template_type,
        enabled=enabled,
        q=q,
        limit=limit,
        offset=offset,
    )


@router.post("", response_model=TemplateRead)
def create_template(payload: TemplateCreate, db: Session = Depends(get_db)) -> Template:
    template = Template(**payload.model_dump())
    TemplateRepository(db).save(template)
    AuditLogger(db).log("create_template", "template", str(template.id), payload.model_dump())
    db.commit()
    db.refresh(template)
    return template


@router.get("/{template_id}", response_model=TemplateRead)
def get_template(template_id: str, db: Session = Depends(get_db)) -> Template:
    template = TemplateRepository(db).get(template_id)
    if template is None:
        raise HTTPException(status_code=404, detail="template not found")
    return template


@router.patch("/{template_id}", response_model=TemplateRead)
def update_template(template_id: str, payload: TemplateUpdate, db: Session = Depends(get_db)) -> Template:
    repository = TemplateRepository(db)
    template = repository.get(template_id)
    if template is None:
        raise HTTPException(status_code=404, detail="template not found")
    TemplateService.apply_update(template, payload)
    AuditLogger(db).log("update_template", "template", str(template.id), payload.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(template)
    return template

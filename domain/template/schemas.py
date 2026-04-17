from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from domain.template.enums import TemplateOwnerType, TemplateType


class TemplateCreate(BaseModel):
    template_type: TemplateType
    name: str
    owner_type: TemplateOwnerType = TemplateOwnerType.SYSTEM
    owner_id: UUID | None = None
    description: str | None = None
    category: str | None = None
    content: str
    variables: dict = {}
    version: int = 1
    is_default: bool = False
    enabled: bool = True


class TemplateUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    content: str | None = None
    variables: dict | None = None
    is_default: bool | None = None
    enabled: bool | None = None


class TemplateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    template_type: TemplateType
    name: str
    owner_type: TemplateOwnerType
    description: str | None = None
    category: str | None = None
    version: int
    is_default: bool
    enabled: bool

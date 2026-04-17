from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from domain.template.enums import TemplateOwnerType, TemplateType


class TemplateCreate(BaseModel):
    template_type: TemplateType
    name: str
    owner_type: TemplateOwnerType = TemplateOwnerType.SYSTEM
    owner_id: UUID | None = None
    content: str
    variables: dict = {}
    version: int = 1
    enabled: bool = True


class TemplateRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    template_type: TemplateType
    name: str
    owner_type: TemplateOwnerType
    version: int
    enabled: bool

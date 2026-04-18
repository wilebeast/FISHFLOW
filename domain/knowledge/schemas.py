from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class KnowledgeCreate(BaseModel):
    product_id: UUID | None = None
    category: str
    question: str
    answer: str
    tags: dict = {}
    enabled: bool = True


class KnowledgeUpdate(BaseModel):
    category: str | None = None
    question: str | None = None
    answer: str | None = None
    tags: dict | None = None
    enabled: bool | None = None


class KnowledgeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    product_id: UUID | None = None
    category: str
    question: str
    answer: str
    tags: dict
    enabled: bool
    updated_at: datetime

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AICopyGeneratePayload(BaseModel):
    scene: str
    title: str | None = None
    product_title: str | None = None
    description: str | None = None
    highlights: str | None = None
    question: str | None = None
    answer: str | None = None
    operator: str = "system"


class AICopyResult(BaseModel):
    content: str


class AICopyHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    scene: str
    input_payload: dict
    output_payload: dict
    operator: str
    created_at: datetime

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AIReplyConfigCreate(BaseModel):
    name: str = "default"
    provider: str = "openai-compatible"
    model: str = "gpt-5-mini"
    system_prompt: str = "You are a concise sales assistant."
    temperature: float = 0.2
    max_tokens: int = 200
    enabled: bool = True
    guardrails_json: dict = {}


class AIReplyConfigUpdate(BaseModel):
    name: str | None = None
    provider: str | None = None
    model: str | None = None
    system_prompt: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    enabled: bool | None = None
    guardrails_json: dict | None = None


class AIReplyTestPayload(BaseModel):
    message: str
    buyer_id: str | None = None
    product_title: str | None = None


class AIReplyConfigRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    provider: str
    model: str
    system_prompt: str
    temperature: float
    max_tokens: int
    enabled: bool
    guardrails_json: dict
    updated_at: datetime


class AICallLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    scene: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: int
    status: str
    request_snapshot: dict
    response_snapshot: dict
    created_at: datetime

from __future__ import annotations

import time

from domain.ai_reply.models import AICallLog, AIReplyConfig
from domain.ai_reply.repository import AICallLogRepository
from domain.ai_reply.schemas import AIReplyConfigUpdate, AIReplyTestPayload


class AIReplyConfigService:
    @staticmethod
    def apply_update(config: AIReplyConfig, payload: AIReplyConfigUpdate) -> AIReplyConfig:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(config, field, value)
        return config


class AIReplyService:
    def __init__(self, log_repository: AICallLogRepository) -> None:
        self.log_repository = log_repository

    def generate_demo_reply(self, config: AIReplyConfig, payload: AIReplyTestPayload) -> dict:
        started = time.perf_counter()
        reply = (
            f"[{config.model}] 您好"
            f"{'，关于 ' + payload.product_title if payload.product_title else ''}，"
            f"{payload.message.strip()}。付款后可自动发货，如需人工处理请直接留言。"
        )
        latency_ms = int((time.perf_counter() - started) * 1000)
        request_snapshot = payload.model_dump()
        response_snapshot = {"reply": reply}
        self.log_repository.save(
            AICallLog(
                scene="ai_reply_test",
                model=config.model,
                input_tokens=len(payload.message),
                output_tokens=len(reply),
                latency_ms=latency_ms,
                status="success",
                request_snapshot=request_snapshot,
                response_snapshot=response_snapshot,
            )
        )
        return response_snapshot

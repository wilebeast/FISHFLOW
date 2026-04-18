from __future__ import annotations

from domain.ai_copy.models import AICopyHistory
from domain.ai_copy.repository import AICopyHistoryRepository
from domain.ai_copy.schemas import AICopyGeneratePayload


class AICopyService:
    def __init__(self, repository: AICopyHistoryRepository) -> None:
        self.repository = repository

    def generate(self, payload: AICopyGeneratePayload) -> dict:
        scene = payload.scene
        if scene == "title":
            content = f"闲鱼热卖 | {payload.product_title or payload.title or '数字商品'} | 自动发货"
        elif scene == "description":
            content = (
                f"{payload.product_title or '该商品'}支持自动发货，"
                f"适合需要快速交付的买家。{payload.highlights or payload.description or ''}"
            ).strip()
        elif scene == "faq":
            content = f"Q: {payload.question or '怎么发货？'}\nA: {payload.answer or '付款后系统自动发货。'}"
        elif scene == "rewrite":
            content = f"您好，{payload.answer or payload.description or '付款后自动发货，如有问题请留言。'}"
        else:
            content = payload.description or payload.highlights or "AI 文案生成结果"

        record = AICopyHistory(
            scene=scene,
            input_payload=payload.model_dump(),
            output_payload={"content": content},
            operator=payload.operator,
        )
        self.repository.save(record)
        return {"content": content}

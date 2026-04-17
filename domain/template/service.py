from __future__ import annotations

from domain.template.models import Template
from domain.template.schemas import TemplateUpdate


class TemplateService:
    @staticmethod
    def render(template: Template, variables: dict[str, object]) -> str:
        content = template.content
        for key, value in variables.items():
            content = content.replace(f"{{{{{key}}}}}", str(value))
        return content

    @staticmethod
    def apply_update(template: Template, payload: TemplateUpdate) -> Template:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(template, field, value)
        return template

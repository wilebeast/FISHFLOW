from __future__ import annotations

from domain.template.models import Template


class TemplateService:
    @staticmethod
    def render(template: Template, variables: dict[str, object]) -> str:
        content = template.content
        for key, value in variables.items():
            content = content.replace(f"{{{{{key}}}}}", str(value))
        return content

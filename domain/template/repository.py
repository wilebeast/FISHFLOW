from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.template.models import Template


class TemplateRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _coerce_uuid(template_id: UUID | str) -> UUID:
        return template_id if isinstance(template_id, UUID) else UUID(str(template_id))

    def get(self, template_id: UUID | str) -> Template | None:
        stmt = select(Template).where(Template.id == self._coerce_uuid(template_id))
        return self.session.scalar(stmt)

    def save(self, template: Template) -> Template:
        self.session.add(template)
        self.session.flush()
        return template

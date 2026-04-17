from __future__ import annotations

from uuid import UUID

from sqlalchemy import desc, select
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

    def list_recent(
        self,
        template_type: str | None = None,
        enabled: bool | None = None,
        q: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Template]:
        stmt = select(Template)
        if template_type:
            stmt = stmt.where(Template.template_type == template_type)
        if enabled is not None:
            stmt = stmt.where(Template.enabled.is_(enabled))
        if q:
            stmt = stmt.where(Template.name.ilike(f"%{q}%"))
        stmt = stmt.order_by(desc(Template.updated_at)).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

    def save(self, template: Template) -> Template:
        self.session.add(template)
        self.session.flush()
        return template

from __future__ import annotations

from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from domain.product.models import Product


class ProductRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    @staticmethod
    def _coerce_uuid(value: UUID | str) -> UUID:
        return value if isinstance(value, UUID) else UUID(str(value))

    def get(self, product_id: UUID | str) -> Product | None:
        stmt = select(Product).where(Product.id == self._coerce_uuid(product_id))
        return self.session.scalar(stmt)

    def get_by_external_product_id(self, external_product_id: str) -> Product | None:
        stmt = select(Product).where(Product.external_product_id == external_product_id)
        return self.session.scalar(stmt)

    def list_recent(
        self,
        q: str | None = None,
        status: str | None = None,
        delivery_mode: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Product]:
        stmt = select(Product)
        if q:
            stmt = stmt.where(Product.title.ilike(f"%{q}%"))
        if status:
            stmt = stmt.where(Product.status == status)
        if delivery_mode:
            stmt = stmt.where(Product.delivery_mode == delivery_mode)
        stmt = stmt.order_by(desc(Product.updated_at)).offset(offset).limit(limit)
        return list(self.session.scalars(stmt).all())

    def save(self, product: Product) -> Product:
        self.session.add(product)
        self.session.flush()
        return product

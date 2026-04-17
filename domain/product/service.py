from __future__ import annotations

from domain.product.models import Product
from domain.product.schemas import ProductUpdate


class ProductService:
    def apply_update(self, product: Product, payload: ProductUpdate) -> Product:
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        return product

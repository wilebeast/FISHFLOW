from __future__ import annotations

from services.channel_adapter.base import ProductChannel
from services.channel_adapter.xianyu.client import XianyuClient


class XianyuProductAdapter(ProductChannel):
    def __init__(self) -> None:
        self.client = XianyuClient()

    async def fetch_products(self, account_ref: str, cursor: str | None = None) -> list[dict]:
        data = await self.client.get("/products", params={"account": account_ref, "cursor": cursor})
        return data.get("items", [])

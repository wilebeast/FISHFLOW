from __future__ import annotations

from services.channel_adapter.base import OrderChannel
from services.channel_adapter.xianyu.client import XianyuClient


class XianyuOrderAdapter(OrderChannel):
    def __init__(self) -> None:
        self.client = XianyuClient()

    async def get_order_detail(self, account_ref: str, order_ref: str) -> dict:
        return await self.client.get("/orders/detail", params={"account": account_ref, "order": order_ref})

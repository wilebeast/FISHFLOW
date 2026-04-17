from __future__ import annotations

from services.channel_adapter.base import MessageChannel
from services.channel_adapter.xianyu.client import XianyuClient


class XianyuMessageAdapter(MessageChannel):
    def __init__(self) -> None:
        self.client = XianyuClient()

    async def fetch_new_messages(self, account_ref: str, cursor: str | None = None) -> list[dict]:
        data = await self.client.get("/messages", params={"account": account_ref, "cursor": cursor})
        return data.get("items", [])

    async def send_message(self, account_ref: str, session_ref: str, content: str) -> dict:
        return await self.client.post(
            "/messages/send",
            {"account": account_ref, "session": session_ref, "content": content},
        )

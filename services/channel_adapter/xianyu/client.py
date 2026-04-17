from __future__ import annotations

import httpx

from infrastructure.config.settings import get_settings


class XianyuClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.xianyu_api_base_url

    async def get(self, path: str, params: dict | None = None) -> dict:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10) as client:
            response = await client.get(path, params=params)
            response.raise_for_status()
            return response.json()

    async def post(self, path: str, payload: dict) -> dict:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=10) as client:
            response = await client.post(path, json=payload)
            response.raise_for_status()
            return response.json()

from __future__ import annotations

import httpx

from infrastructure.config.settings import get_settings


class XianyuClient:
    def __init__(self) -> None:
        settings = get_settings()
        self.base_url = settings.xianyu_bridge_api_base_url or settings.xianyu_api_base_url
        self.timeout = settings.xianyu_timeout_seconds
        self.token = settings.xianyu_bridge_token

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    async def get(self, path: str, params: dict | None = None) -> dict:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            response = await client.get(path, params=params, headers=self._headers())
            response.raise_for_status()
            return response.json()

    async def post(self, path: str, payload: dict) -> dict:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            response = await client.post(path, json=payload, headers=self._headers())
            response.raise_for_status()
            return response.json()

from __future__ import annotations

from abc import ABC, abstractmethod


class MessageChannel(ABC):
    @abstractmethod
    async def fetch_new_messages(self, account_ref: str, cursor: str | None = None) -> list[dict]:
        raise NotImplementedError

    @abstractmethod
    async def send_message(self, account_ref: str, session_ref: str, content: str) -> dict:
        raise NotImplementedError


class OrderChannel(ABC):
    @abstractmethod
    async def get_order_detail(self, account_ref: str, order_ref: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def fetch_orders(self, account_ref: str, cursor: str | None = None) -> list[dict]:
        raise NotImplementedError


class ProductChannel(ABC):
    @abstractmethod
    async def fetch_products(self, account_ref: str, cursor: str | None = None) -> list[dict]:
        raise NotImplementedError

"""
Клиент для FIAS Public API (Python, асинхронный)

Библиотека для работы с публичным API ФИАС (Федеральная информационная адресная система).
Предоставляет простой доступ к функциям поиска адресов и получения детальной информации с поддержкой async/await.

Пример:
    >>> import asyncio
    >>> from fias_public_api import AsyncFPA, get_token_async
    >>> async def main():
    ...     token = await get_token_async()
    ...     async with AsyncFPA(token) as api:
    ...         results = await api.search("Москва, Красная площадь")
    ...         details = await api.details(12345)
    >>> asyncio.run(main())
"""

import httpx
from .constants import STANDART_HEADERS

async def get_token_async(url="https://fias.nalog.ru/"):
    """Получить токен аутентификации из сервиса ФИАС.

    Args:
        url (str): Базовый URL сервиса ФИАС

    Returns:
        str: Токен аутентификации

    Raises:
        ValueError: Если не удалось получить токен
        httpx.HTTPError: Если HTTP запрос завершился ошибкой
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://fias.nalog.ru/Home/GetSpasSettings", params={"url": url}
        )
        response.raise_for_status()
        if response.status_code != 200:
            raise ValueError("Не удалось получить токен")
        return response.json()["Token"]


class AsyncFPA:
    """Основной класс клиента для работы с FIAS Public API (асинхронный).

    Этот класс предоставляет методы для поиска адресов и получения детальной информации
    об адресных объектах в системе ФИАС с поддержкой асинхронных операций.

    Args:
        token (str): Токен аутентификации для доступа к API
    """

    def __init__(self, token: str):
        self.token = token
        self._client = None

    async def __aenter__(self):
        """Вход в асинхронный контекстный менеджер."""
        self._client = httpx.AsyncClient()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Выход из асинхронного контекстного менеджера."""
        if self._client:
            await self._client.aclose()

    @property
    def client(self):
        """Получить или создать httpx клиент."""
        if self._client is None:
            self._client = httpx.AsyncClient()
        return self._client

    async def details(self, object_id: int):
        """Получить детальную информацию об адресном объекте по его ID.

        Args:
            object_id (int): ID объекта ФИАС

        Returns:
            dict: Детальная информация об адресном объекте

        Raises:
            httpx.HTTPError: Если HTTP запрос завершился ошибкой
        """
        response = await self.client.get(
            "https://fias-public-service.nalog.ru/api/spas/v2.0/GetAddressItemById",
            params={"object_id": object_id, "address_type": 2},
            headers=STANDART_HEADERS(self.token),
        )
        response.raise_for_status()
        return response.json()

    async def search(
        self,
        search_string: str,
        url: str = "https://fias-public-service.nalog.ru/api/spas/v2.0/GetAddressHint",
    ):
        """Поиск адресов по текстовой строке.

        Args:
            search_string (str): Текст для поиска (адрес, улица и т.д.)
            url (str): URL конечной точки API для поиска

        Returns:
            list: Список подсказок адресов, соответствующих поисковому запросу

        Raises:
            httpx.HTTPError: Если HTTP запрос завершился ошибкой
        """
        search_string = search_string.encode("utf-8").decode("utf-8")
        payload = {
            "searchString": search_string,
            "addressType": 2,
            "searchNonActive": False,
        }
        response = await self.client.post(
            url, json=payload, headers=STANDART_HEADERS(self.token)
        )
        response.raise_for_status()

        return response.json()["hints"]

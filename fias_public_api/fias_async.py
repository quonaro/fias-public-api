"""
FIAS Public API Python Client (Async)

A Python client library for interacting with the Russian FIAS (Federal Information Address System) Public API.
Provides easy access to address search and details functionality with async/await support.

Example:
    >>> import asyncio
    >>> from fias_public_api.async import FiasPublicApi
    >>> async def main():
    ...     api = FiasPublicApi("your_token")
    ...     results = await api.search("Москва, Красная площадь")
    ...     details = await api.details(12345)
    >>> asyncio.run(main())
"""

import httpx
from .constants import STANDART_HEADERS

async def get_token_async(url="https://fias.nalog.ru/"):
    """Get authentication token from FIAS service.

    Args:
        url (str): Base URL for FIAS service

    Returns:
        str: Authentication token

    Raises:
        ValueError: If token retrieval fails
        httpx.HTTPError: If HTTP request fails
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://fias.nalog.ru/Home/GetSpasSettings", params={"url": url}
        )
        response.raise_for_status()
        if response.status_code != 200:
            raise ValueError("Failed to get token")
        return response.json()["Token"]


class AsyncFPA:
    """Main client class for FIAS Public API operations.

    This class provides methods to search addresses and get detailed information
    about address objects in the Russian FIAS system.

    Args:
        token (str): Authentication token for API access
    """

    def __init__(self, token: str):
        self.token = token
        self._client = None

    async def __aenter__(self):
        """Async context manager entry."""
        self._client = httpx.AsyncClient()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()

    @property
    def client(self):
        """Get or create httpx client."""
        if self._client is None:
            self._client = httpx.AsyncClient()
        return self._client

    async def details(self, object_id: int):
        """Get detailed information about an address object by its ID.

        Args:
            object_id (int): FIAS object ID

        Returns:
            dict: Address object details

        Raises:
            httpx.HTTPError: If HTTP request fails
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
        """Search for addresses by text string.

        Args:
            search_string (str): Text to search for (address, street, etc.)
            url (str): API endpoint URL for search

        Returns:
            list: List of address hints matching the search

        Raises:
            httpx.HTTPError: If HTTP request fails
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

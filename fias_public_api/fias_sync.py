"""
FIAS Public API Python Client

A Python client library for interacting with the Russian FIAS (Federal Information Address System) Public API.
Provides easy access to address search and details functionality.

Example:
    >>> from fias_public_api import FiasPublicApi
    >>> api = FiasPublicApi("your_token")
    >>> results = api.search("Москва, Красная площадь")
    >>> details = api.details(12345)
"""

import requests
from .constants import STANDART_HEADERS

def get_token_sync(url="https://fias.nalog.ru/"):
    """Get authentication token from FIAS service.

    Args:
        url (str): Base URL for FIAS service

    Returns:
        str: Authentication token

    Raises:
        ValueError: If token retrieval fails
        requests.HTTPError: If HTTP request fails
    """
    response = requests.get(
        "https://fias.nalog.ru/Home/GetSpasSettings", params={"url": url}
    )
    response.raise_for_status()
    if response.status_code != 200:
        raise ValueError("Failed to get token")
    return response.json()["Token"]


class SyncFPA:
    """Main client class for FIAS Public API operations.

    This class provides methods to search addresses and get detailed information
    about address objects in the Russian FIAS system.

    Args:
        token (str): Authentication token for API access
    """

    def __init__(self, token: str):
        self.token = token

    def details(self, object_id: int):
        """Get detailed information about an address object by its ID.

        Args:
            object_id (int): FIAS object ID

        Returns:
            dict: Address object details

        Raises:
            requests.HTTPError: If HTTP request fails
        """
        response = requests.get(
            "https://fias-public-service.nalog.ru/api/spas/v2.0/GetAddressItemById",
            params={"object_id": object_id, "address_type": 2},
            headers=STANDART_HEADERS(self.token),
        )
        response.raise_for_status()
        return response.json()

    def search(
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
            requests.HTTPError: If HTTP request fails
        """
        search_string = search_string.encode("utf-8").decode("utf-8")
        payload = {
            "searchString": search_string,
            "addressType": 2,
            "searchNonActive": False,
        }
        response = requests.post(
            url, json=payload, headers=STANDART_HEADERS(self.token)
        )
        response.raise_for_status()

        return response.json()["hints"]

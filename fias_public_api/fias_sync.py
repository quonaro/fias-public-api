"""
Клиент для FIAS Public API (Python)

Библиотека для работы с публичным API ФИАС (Федеральная информационная адресная система).
Предоставляет простой доступ к функциям поиска адресов и получения детальной информации.

Пример:
    >>> from fias_public_api import SyncFPA, get_token_sync
    >>> token = get_token_sync()
    >>> api = SyncFPA(token)
    >>> results = api.search("Москва, Красная площадь")
    >>> details = api.details(12345)
"""

import requests
from .constants import STANDART_HEADERS, AddressType


def get_token_sync(url="https://fias.nalog.ru/"):
    """Получить токен аутентификации из сервиса ФИАС.

    Args:
        url (str): Базовый URL сервиса ФИАС

    Returns:
        str: Токен аутентификации

    Raises:
        ValueError: Если не удалось получить токен
        requests.HTTPError: Если HTTP запрос завершился ошибкой
    """
    response = requests.get(
        "https://fias.nalog.ru/Home/GetSpasSettings", params={"url": url}
    )
    response.raise_for_status()
    if response.status_code != 200:
        raise ValueError("Не удалось получить токен")
    return response.json()["Token"]


class SyncFPA:
    """Основной класс клиента для работы с FIAS Public API.

    Этот класс предоставляет методы для поиска адресов и получения детальной информации
    об адресных объектах в системе ФИАС.

    Args:
        token (str): Токен аутентификации для доступа к API
    """

    def __init__(self, token: str):
        self.token = token

    def details_by_id(self, object_id: int, address_type: int | AddressType = 2):
        """Получить детальную информацию об адресном объекте по его ID.

        Args:
            object_id (int): ID объекта ФИАС
            address_type (int | AddressType): Тип адреса (по умолчанию 2)

        Returns:
            dict: Детальная информация об адресном объекте

        Raises:
            requests.HTTPError: Если HTTP запрос завершился ошибкой
        """
        response = requests.get(
            "https://fias-public-service.nalog.ru/api/spas/v2.0/GetAddressItemById",
            params={"object_id": object_id, "address_type": address_type},
            headers=STANDART_HEADERS(self.token),
        )
        response.raise_for_status()
        return response.json()

    def details_by_guid(self, object_guid: str, address_type: int | AddressType = 2):
        """Получить детальную информацию об адресном объекте по его GUID.
        Args:
            object_guid (str): GUID объекта ФИАС
            address_type (int | AddressType): Тип адреса (по умолчанию 2)

        Returns:
            dict: Детальная информация об адресном объекте
        """
        response = requests.get(
            "https://fias-public-service.nalog.ru/api/spas/v2.0/GetAddressItemByGuid",
            params={"object_guid": object_guid, "address_type": address_type},
            headers=STANDART_HEADERS(self.token),
        )
        response.raise_for_status()
        return response.json()

    def details(self, object_id: int, address_type: int | AddressType = 2):
        print("details устарел, используйте details_by_id вместо этого")
        return self.details_by_id(object_id, address_type)

    def search(
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
            requests.HTTPError: Если HTTP запрос завершился ошибкой
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

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
from .constants import (
    STANDART_HEADERS,
    AddressType,
    TOKEN_URL,
    GET_REGIONS,
    GET_ADDRESS_ITEMS,
    GET_DETAILS,
    IS_DESCENDANT,
    HAS_DESCENDANTS,
    GET_ADDRESS_ITEM_BY_ID,
    GET_ADDRESS_ITEM_BY_GUID,
    GET_ADDRESS_ITEM_BY_CADASTRAL_NUMBER,
    GET_FIAS_OBJECT_TYPES,
    SEARCH_ADDRESS_ITEMS,
    GET_ADDRESS_HINT,
    SEARCH_ADDRESS_ITEM,
    GET_LOCATION_BY_IP,
)


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
    response = requests.get(TOKEN_URL, params={"url": url})
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
        address_type (int | AddressType, optional): Тип адреса по умолчанию (по умолчанию 2 - MUNICIPALITY)
    """

    def __init__(self, token: str, address_type: int | AddressType = 2):
        self.token = token
        self.address_type = address_type

    def _get_address_type(self, address_type: int | AddressType | None) -> int:
        """Получить тип адреса, используя значение по умолчанию из конструктора если не указано."""
        if address_type is None:
            return self.address_type
        return int(address_type)

    def get_regions(self):
        """Получить список регионов.

        Returns:
            dict: Список регионов

        Raises:
            requests.HTTPError: Если HTTP запрос завершился ошибкой
        """
        response = requests.get(
            GET_REGIONS, headers=STANDART_HEADERS(self.token)
        )
        response.raise_for_status()
        return response.json()

    def get_address_items(
        self,
        path: str | None = None,
        address_level: int | None = None,
        address_levels: list[int] | None = None,
        name_part: str | None = None,
        address_type: int | AddressType | None = None,
        include_descendants: bool | None = None,
    ):
        """Получить список дочерних элементов, соответствующих заданным фильтрам.

        Args:
            path (str, optional): Путь к родительскому элементу
            address_level (int, optional): Уровень адреса
            address_levels (list[int], optional): Список уровней адресов
            name_part (str, optional): Часть названия для поиска
            address_type (int | AddressType, optional): Тип адреса
            include_descendants (bool, optional): Включать ли дочерние элементы

        Returns:
            dict: Список адресных элементов

        Raises:
            requests.HTTPError: Если HTTP запрос завершился ошибкой
        """
        payload = {}
        if path is not None:
            payload["path"] = path
        if address_level is not None:
            payload["address_level"] = address_level
        if address_levels is not None:
            payload["address_levels"] = address_levels
        if name_part is not None:
            payload["name_part"] = name_part
        if address_type is not None:
            payload["address_type"] = self._get_address_type(address_type)
        elif self.address_type:
            payload["address_type"] = self.address_type
        if include_descendants is not None:
            payload["include_descendants"] = include_descendants

        response = requests.post(
            GET_ADDRESS_ITEMS, json=payload, headers=STANDART_HEADERS(self.token)
        )
        response.raise_for_status()
        return response.json()

    def get_details(self, object_id: int):
        """Получить дополнительную информацию для заданного адресного элемента.

        Args:
            object_id (int): Идентификатор адресного элемента

        Returns:
            dict: Дополнительная информация об адресном элементе

        Raises:
            requests.HTTPError: Если HTTP запрос завершился ошибкой
        """
        response = requests.get(
            GET_DETAILS,
            params={"object_id": object_id},
            headers=STANDART_HEADERS(self.token),
        )
        response.raise_for_status()
        return response.json()

    def is_descendant(
        self,
        ancestor: int,
        descendant: int,
        address_type: int | AddressType | None = None,
    ):
        """Проверка, является ли элемент ancestor родительским элементом в иерархии для элемента descendant.

        Args:
            ancestor (int): Идентификатор родительского элемента
            descendant (int): Идентификатор дочернего элемента
            address_type (int | AddressType, optional): Вид представления адреса

        Returns:
            dict: Результат проверки

        Raises:
            requests.HTTPError: Если HTTP запрос завершился ошибкой
        """
        params = {"ancestor": ancestor, "descendant": descendant}
        if address_type is not None:
            params["address_type"] = self._get_address_type(address_type)
        elif self.address_type:
            params["address_type"] = self.address_type

        response = requests.get(
            IS_DESCENDANT, params=params, headers=STANDART_HEADERS(self.token)
        )
        response.raise_for_status()
        return response.json()

    def has_descendants(
        self,
        parent: int,
        up_to_level: int,
        address_type: int | AddressType | None = None,
    ):
        """Проверка, имеет ли элемент parent дочерние элементы до уровня up_to_level.

        Args:
            parent (int): Идентификатор родительского элемента
            up_to_level (int): Максимальный уровень дочерних элементов
            address_type (int | AddressType, optional): Вид представления адреса

        Returns:
            dict: Результат проверки

        Raises:
            requests.HTTPError: Если HTTP запрос завершился ошибкой
        """
        params = {"parent": parent, "up_to_level": up_to_level}
        if address_type is not None:
            params["address_type"] = self._get_address_type(address_type)
        elif self.address_type:
            params["address_type"] = self.address_type

        response = requests.get(
            HAS_DESCENDANTS, params=params, headers=STANDART_HEADERS(self.token)
        )
        response.raise_for_status()
        return response.json()

    def details_by_id(
        self, object_id: int, address_type: int | AddressType | None = None
    ):
        """Получить детальную информацию об адресном объекте по его ID.

        Args:
            object_id (int): ID объекта ФИАС
            address_type (int | AddressType, optional): Тип адреса

        Returns:
            dict: Детальная информация об адресном объекте

        Raises:
            requests.HTTPError: Если HTTP запрос завершился ошибкой
        """
        params = {"object_id": object_id}
        if address_type is not None:
            params["address_type"] = self._get_address_type(address_type)
        elif self.address_type:
            params["address_type"] = self.address_type

        response = requests.get(
            GET_ADDRESS_ITEM_BY_ID, params=params, headers=STANDART_HEADERS(self.token)
        )
        response.raise_for_status()
        return response.json()

    def details_by_guid(
        self, object_guid: str, address_type: int | AddressType | None = None
    ):
        """Получить детальную информацию об адресном объекте по его GUID.

        Args:
            object_guid (str): GUID объекта ФИАС
            address_type (int | AddressType, optional): Тип адреса

        Returns:
            dict: Детальная информация об адресном объекте

        Raises:
            requests.HTTPError: Если HTTP запрос завершился ошибкой
        """
        params = {"object_guid": object_guid}
        if address_type is not None:
            params["address_type"] = self._get_address_type(address_type)
        elif self.address_type:
            params["address_type"] = self.address_type

        response = requests.get(
            GET_ADDRESS_ITEM_BY_GUID,
            params=params,
            headers=STANDART_HEADERS(self.token),
        )
        response.raise_for_status()
        return response.json()

    def get_address_item_by_cadastral_number(
        self, cadastral_number: str, address_type: int | AddressType | None = None
    ):
        """Получение адресного элемента по кадастровому номеру.

        Args:
            cadastral_number (str): Кадастровый номер
            address_type (int | AddressType, optional): Тип адреса

        Returns:
            dict: Адресный элемент

        Raises:
            requests.HTTPError: Если HTTP запрос завершился ошибкой
        """
        params = {"cadastral_number": cadastral_number}
        if address_type is not None:
            params["address_type"] = self._get_address_type(address_type)
        elif self.address_type:
            params["address_type"] = self.address_type

        response = requests.get(
            GET_ADDRESS_ITEM_BY_CADASTRAL_NUMBER,
            params=params,
            headers=STANDART_HEADERS(self.token),
        )
        response.raise_for_status()
        return response.json()

    def get_fias_object_types(self):
        """Получение типов объектов ФИАС.

        Returns:
            dict: Список типов объектов ФИАС

        Raises:
            requests.HTTPError: Если HTTP запрос завершился ошибкой
        """
        response = requests.get(
            GET_FIAS_OBJECT_TYPES, headers=STANDART_HEADERS(self.token)
        )
        response.raise_for_status()
        return response.json()

    def search_address_items(
        self, search_string: str, address_type: int | AddressType | None = None
    ):
        """Получение адресных элементов, соответствующих заданной произвольной строке адреса.

        Args:
            search_string (str): Адрес строкой
            address_type (int | AddressType, optional): Вид представления адреса

        Returns:
            dict: Список адресных элементов

        Raises:
            ValueError: Если search_string пустая строка
            requests.HTTPError: Если HTTP запрос завершился ошибкой
        """
        if not search_string.strip():
            raise ValueError("search_string cannot be empty")
        
        params = {"search_string": search_string}
        if address_type is not None:
            params["address_type"] = self._get_address_type(address_type)
        elif self.address_type:
            params["address_type"] = self.address_type

        response = requests.get(
            SEARCH_ADDRESS_ITEMS, params=params, headers=STANDART_HEADERS(self.token)
        )
        response.raise_for_status()
        return response.json()

    def get_address_hint(
        self,
        search_string: str | None = None,
        address_type: int | AddressType | None = None,
        up_to_level: int | None = None,
        locations_boost: int | None = None,
        search_non_active: bool = False,
    ):
        """Сервис для организации стандартизированного ввода и поиска адреса (унифицированная адресная строка).

        Args:
            search_string (str, optional): Адрес строкой
            address_type (int | AddressType, optional): Вид представления адреса
            up_to_level (int, optional): Максимальный уровень поиска
            locations_boost (int, optional): Приоритет локаций
            search_non_active (bool): Искать неактивные адреса

        Returns:
            dict: Список подсказок адресов

        Raises:
            ValueError: Если search_string пустая строка
            requests.HTTPError: Если HTTP запрос завершился ошибкой
        """
        if search_string is not None:
            # Validate search_string is not empty
            if not search_string.strip():
                raise ValueError("search_string cannot be empty")
            # GET request
            params = {"search_string": search_string}
            if address_type is not None:
                params["address_type"] = self._get_address_type(address_type)
            elif self.address_type:
                params["address_type"] = self.address_type

            response = requests.get(
                GET_ADDRESS_HINT, params=params, headers=STANDART_HEADERS(self.token)
            )
        else:
            # POST request
            payload = {"searchNonActive": search_non_active}
            if address_type is not None:
                payload["addressType"] = self._get_address_type(address_type)
            elif self.address_type:
                payload["addressType"] = self.address_type
            if up_to_level is not None:
                payload["upToLevel"] = up_to_level
            if locations_boost is not None:
                payload["locationsBoost"] = locations_boost

            response = requests.post(
                GET_ADDRESS_HINT, json=payload, headers=STANDART_HEADERS(self.token)
            )

        response.raise_for_status()
        return response.json()

    def search_address_item(
        self, search_string: str, address_type: int | AddressType | None = None
    ):
        """Получение адресного элемента, соответствующего заданной произвольной строке адреса.

        Args:
            search_string (str): Адрес строкой
            address_type (int | AddressType, optional): Вид представления адреса

        Returns:
            dict: Адресный элемент

        Raises:
            ValueError: Если search_string пустая строка
            requests.HTTPError: Если HTTP запрос завершился ошибкой
        """
        if not search_string.strip():
            raise ValueError("search_string cannot be empty")
        
        params = {"search_string": search_string}
        if address_type is not None:
            params["address_type"] = self._get_address_type(address_type)
        elif self.address_type:
            params["address_type"] = self.address_type

        response = requests.get(
            SEARCH_ADDRESS_ITEM, params=params, headers=STANDART_HEADERS(self.token)
        )
        response.raise_for_status()
        return response.json()

    def get_location_by_ip(
        self, ip: str, address_type: int | AddressType | None = None
    ):
        """Получение населённого пункта по IP адресу.

        Args:
            ip (str): IP адрес
            address_type (int | AddressType, optional): Тип представления возвращаемых адресных объектов

        Returns:
            dict: Адресные объекты

        Raises:
            requests.HTTPError: Если HTTP запрос завершился ошибкой
        """
        params = {"ip": ip}
        if address_type is not None:
            params["address_type"] = self._get_address_type(address_type)
        elif self.address_type:
            params["address_type"] = self.address_type

        response = requests.get(
            GET_LOCATION_BY_IP, params=params, headers=STANDART_HEADERS(self.token)
        )
        response.raise_for_status()
        return response.json()

    def details(self, object_id: int, address_type: int | AddressType | None = None):
        """Устаревший метод. Используйте details_by_id вместо этого."""
        print("details устарел, используйте details_by_id вместо этого")
        return self.details_by_id(object_id, address_type)

    def search(
        self,
        search_string: str,
        address_type: int | AddressType | None = None,
    ):
        """Поиск адресов по текстовой строке (обертка над get_address_hint).

        Args:
            search_string (str): Текст для поиска (адрес, улица и т.д.)
            address_type (int | AddressType, optional): Тип адреса

        Returns:
            list: Список подсказок адресов, соответствующих поисковому запросу

        Raises:
            ValueError: Если search_string пустая строка
            requests.HTTPError: Если HTTP запрос завершился ошибкой
        """
        result = self.get_address_hint(search_string=search_string, address_type=address_type)
        return result.get("hints", [])

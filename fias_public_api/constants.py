from enum import IntEnum
from functools import wraps
import time
import inspect
from typing import Callable, TypeVar, ParamSpec

# Base URLs
BASE_URL = "https://fias-public-service.nalog.ru/api/spas/v2.0"
TOKEN_URL = "https://fias.nalog.ru/Home/GetSpasSettings"

# AddressInfo endpoints
GET_REGIONS = f"{BASE_URL}/GetRegions"
GET_ADDRESS_ITEMS = f"{BASE_URL}/GetAddressItems"
GET_DETAILS = f"{BASE_URL}/GetDetails"
IS_DESCENDANT = f"{BASE_URL}/IsDescendant"
HAS_DESCENDANTS = f"{BASE_URL}/HasDescendants"
GET_ADDRESS_ITEM_BY_ID = f"{BASE_URL}/GetAddressItemById"
GET_ADDRESS_ITEM_BY_GUID = f"{BASE_URL}/GetAddressItemByGuid"
GET_ADDRESS_ITEM_BY_CADASTRAL_NUMBER = f"{BASE_URL}/GetAddressItemByCadastralNumber"
GET_FIAS_OBJECT_TYPES = f"{BASE_URL}/GetFiasObjectTypes"

# Search endpoints
SEARCH_ADDRESS_ITEMS = f"{BASE_URL}/SearchAddressItems"
GET_ADDRESS_HINT = f"{BASE_URL}/GetAddressHint"
SEARCH_ADDRESS_ITEM = f"{BASE_URL}/SearchAddressItem"

# Location endpoints
GET_LOCATION_BY_IP = f"{BASE_URL}/GetLocationByIP"

# Default exceptions for retry decorator
# Note: First request to FIAS API often returns 500 error or ConnectionResetError
DEFAULT_RETRY_EXCEPTIONS = (
    Exception,  # Catch all exceptions by default
)

# Sync-specific exceptions
SYNC_RETRY_EXCEPTIONS = (
    ConnectionResetError,
    OSError,
)

# Async-specific exceptions  
ASYNC_RETRY_EXCEPTIONS = (
    ConnectionResetError,
    OSError,
)


def STANDART_HEADERS(token):
    """Создать стандартные заголовки для HTTP запросов к API ФИАС.

    Args:
        token (str): Токен аутентификации

    Returns:
        dict: Словарь с заголовками для HTTP запросов
    """
    return {
        "accept": "application/json",
        "master-token": token,
        "Content-Type": "application/json",
    }


class AddressType(IntEnum):
    """Типы адресов в системе ФИАС.
    ADMINISTRATIVE - Административный тип
    MUNICIPALITY - Муниципальный тип
    """

    ADMINISTRATIVE = 1
    MUNICIPALITY = 2


P = ParamSpec("P")
R = TypeVar("R")


def retry_on_error(
    max_retries: int = 3,
    delay: float = 0.5,
    backoff: float = 2.0,
    exceptions: tuple | None = None,
):
    """Декоратор для повторных попыток при ошибках.
    
    Примечание: Первый запрос к API ФИАС часто возвращает 500 ошибку или ConnectionResetError,
    поэтому декоратор автоматически повторяет запрос при возникновении ошибок.

    Args:
        max_retries (int): Максимальное количество попыток (по умолчанию 3)
        delay (float): Начальная задержка между попытками в секундах (по умолчанию 0.5)
        backoff (float): Множитель для увеличения задержки (по умолчанию 2.0)
        exceptions (tuple | None): Кортеж исключений, при которых нужно повторять попытку
                                    (по умолчанию Exception - все исключения)

    Returns:
        Callable: Декорированная функция
    """
    if exceptions is None:
        exceptions = DEFAULT_RETRY_EXCEPTIONS

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        if inspect.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                import asyncio

                current_delay = delay
                last_exception = None

                for attempt in range(max_retries):
                    try:
                        return await func(*args, **kwargs)
                    except exceptions as e:
                        last_exception = e
                        if attempt < max_retries - 1:
                            await asyncio.sleep(current_delay)
                            current_delay *= backoff
                        else:
                            raise

                if last_exception:
                    raise last_exception

            return async_wrapper
        else:
            @wraps(func)
            def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                current_delay = delay
                last_exception = None

                for attempt in range(max_retries):
                    try:
                        return func(*args, **kwargs)
                    except exceptions as e:
                        last_exception = e
                        if attempt < max_retries - 1:
                            time.sleep(current_delay)
                            current_delay *= backoff
                        else:
                            raise

                if last_exception:
                    raise last_exception

            return sync_wrapper

    return decorator
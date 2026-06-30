import json
import logging
from enum import IntEnum
from functools import wraps
import time
import inspect
from typing import Callable, TypeVar, ParamSpec


class JsonFormatter(logging.Formatter):
    """Format log records as JSON lines."""

    def format(self, record):
        log_record = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "msg": record.getMessage(),
        }
        if hasattr(record, "data") and isinstance(record.data, dict):
            log_record.update(record.data)
        return json.dumps(log_record, ensure_ascii=False, default=str)

    def formatTime(self, record):
        created = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(record.created))
        msec = int(record.msecs)
        tz = time.strftime("%z", time.localtime(record.created))
        if tz:
            tz = tz[:3] + ":" + tz[3:]
        return f"{created}.{msec:03d}{tz}"


def _safe_headers(headers):
    """Mask sensitive header values."""
    result = {}
    for k, v in headers.items():
        lk = k.lower()
        if "token" in lk or "secret" in lk or "authorization" in lk:
            result[k] = "[REDACTED]"
        else:
            result[k] = v
    return result


def _truncate_body(body, max_len=1000):
    """Truncate body string for logging."""
    s = str(body)
    if len(s) > max_len:
        return s[:max_len] + "..."
    return s


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


def log_method_call(level=logging.DEBUG):
    """Log method entry, success and exceptions."""

    def decorator(func):
        is_async = inspect.iscoroutinefunction(func)
        func_name = func.__name__

        if is_async:

            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                logger = getattr(args[0], "_logger", None) if args else None
                if logger and logger.isEnabledFor(level):
                    safe_kwargs = {
                        k: v for k, v in kwargs.items() if "token" not in k.lower()
                    }
                    logger.log(
                        level,
                        "%s.%s called with args=%r kwargs=%r",
                        type(args[0]).__name__,
                        func_name,
                        args[1:],
                        safe_kwargs,
                    )
                try:
                    result = await func(*args, **kwargs)
                    if logger and logger.isEnabledFor(level):
                        logger.log(
                            level,
                            "%s.%s completed successfully",
                            type(args[0]).__name__,
                            func_name,
                        )
                    return result
                except Exception as exc:
                    if logger and logger.isEnabledFor(level):
                        logger.log(
                            level,
                            "%s.%s raised %s: %s",
                            type(args[0]).__name__,
                            func_name,
                            type(exc).__name__,
                            exc,
                        )
                    raise

            return async_wrapper
        else:

            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                logger = getattr(args[0], "_logger", None) if args else None
                if logger and logger.isEnabledFor(level):
                    safe_kwargs = {
                        k: v for k, v in kwargs.items() if "token" not in k.lower()
                    }
                    logger.log(
                        level,
                        "%s.%s called with args=%r kwargs=%r",
                        type(args[0]).__name__,
                        func_name,
                        args[1:],
                        safe_kwargs,
                    )
                try:
                    result = func(*args, **kwargs)
                    if logger and logger.isEnabledFor(level):
                        logger.log(
                            level,
                            "%s.%s completed successfully",
                            type(args[0]).__name__,
                            func_name,
                        )
                    return result
                except Exception as exc:
                    if logger and logger.isEnabledFor(level):
                        logger.log(
                            level,
                            "%s.%s raised %s: %s",
                            type(args[0]).__name__,
                            func_name,
                            type(exc).__name__,
                            exc,
                        )
                    raise

            return sync_wrapper

    return decorator


def retry_on_error(
    max_retries: int = 3,
    delay: float = 0.5,
    backoff: float = 2.0,
    exceptions: tuple | None = None,
):
    """Декоратор для повторных попыток при ошибках.

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

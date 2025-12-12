from enum import IntEnum


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
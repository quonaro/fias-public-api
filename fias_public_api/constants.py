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
# Клиент ФИАС Public API на Python

Python-клиент для ФИАС Public API — федеральной информационной адресной системы Российской Федерации. Поддерживает синхронные и асинхронные операции.

## Установка

### Установка из PyPI (рекомендуется)

```bash
pip install fias-public-api
```

### Установка из GitHub

```bash
pip install git+https://github.com/quonaro/fias-public-api
```

### Зависимости

| Пакет      | Версия     | Описание                       |
| ---------- | ---------- | ------------------------------ |
| `requests` | `>=2.32.5` | HTTP библиотека для API запросов |
| `httpx`    | `>=0.28.1` | Асинхронная HTTP библиотека    |

## Быстрый старт

### Синхронный пример

```python
from fias_public_api import get_token_sync, SyncFPA

# Получаем токен автоматически
token = get_token_sync()

# Создаем клиент
api = SyncFPA(token)

# Ищем адрес
results = api.search("Москва, Красная площадь")
print(f"Найдено: {len(results)} результатов")

# Получаем детали первого результата
if results:
    details = api.details_by_id(results[0]['id'])
    print(f"Адрес: {details.get('address', 'N/A')}")
```

### Асинхронный пример

```python
import asyncio
from fias_public_api import get_token_async, AsyncFPA

async def main():
    token = await get_token_async()

    async with AsyncFPA(token) as api:
        results = await api.search("Москва, Красная площадь")
        print(f"Найдено: {len(results)} результатов")

        if results:
            details = await api.details_by_id(results[0]['id'])
            print(f"Адрес: {details.get('address', 'N/A')}")

asyncio.run(main())
```

## Примеры использования

### Поиск адресов

```python
# Простой поиск
results = api.search("Москва")

# Поиск с кастомным URL
results = api.search("Санкт-Петербург", url="https://custom-fias.ru/api")

# Обработка результатов
for result in results:
    print(f"ID: {result['id']}")
    print(f"Адрес: {result['address']}")
    print(f"Тип: {result['type']}")
```

### Получение деталей объекта

```python
from fias_public_api import AddressType

# По ID
object_id = 12345
details = api.details_by_id(object_id, address_type=AddressType.MUNICIPALITY)

# По GUID
object_guid = "some-guid-string"
details = api.details_by_guid(object_guid, address_type=AddressType.ADMINISTRATIVE)
```

### Обработка ошибок

```python
from requests.exceptions import HTTPError, RequestException

try:
    results = api.search("Несуществующий адрес")
except HTTPError as e:
    if e.response.status_code == 404:
        print("Адрес не найден")
    elif e.response.status_code == 401:
        print("Неверный токен")
    else:
        print(f"HTTP ошибка: {e}")
except RequestException as e:
    print(f"Ошибка сети: {e}")
```

### Retry-декоратор

```python
from fias_public_api import retry_on_error
from requests.exceptions import ConnectionError, HTTPError

@retry_on_error(
    max_retries=5,
    delay=1.0,
    backoff=2.0,
    exceptions=(ConnectionError, HTTPError)
)
def search_with_retry(search_string):
    return api.search_address_items(search_string)
```

## Методы API

### Синхронные методы (`SyncFPA`)

- `search(search_string, url)` — поиск адресов по текстовой строке
- `details_by_id(object_id, address_type)` — детали по ID
- `details_by_guid(object_guid, address_type)` — детали по GUID
- `get_regions()` — список регионов
- `get_address_items(...)` — фильтрация адресных объектов
- `get_details(object_id)` — дополнительные сведения
- `is_descendant(ancestor, descendant, address_type)` — проверка вложенности
- `has_descendants(parent, up_to_level, address_type)` — проверка наличия потомков
- `get_address_item_by_cadastral_number(number, address_type)` — по кадастровому номеру
- `get_fias_object_types()` — типы объектов ФИАС
- `search_address_items(search_string, address_type)` — поиск по строке
- `get_address_hint(...)` — подсказки по адресу
- `search_address_item(search_string, address_type)` — поиск одного объекта
- `get_location_by_ip(ip, address_type)` — местоположение по IP

### Асинхронные методы (`AsyncFPA`)

Все методы из `SyncFPA` доступны в асинхронной версии с поддержкой `async`/`await`.

### Вспомогательные функции

- `get_token_sync(url)` — получить токен (синхронно)
- `get_token_async(url)` — получить токен (асинхронно)
- `STANDART_HEADERS(token)` — стандартные HTTP-заголовки
- `AddressType` — перечисление типов адресов (`ADMINISTRATIVE = 1`, `MUNICIPALITY = 2`)
- `retry_on_error(...)` — декоратор для повторных попыток при ошибках

## Примеры из папки examples

Все примеры доступны в папке [`examples/`](examples/):

- **01_basic_usage.py** — базовое использование API
- **02_address_types.py** — работа с типами адресов
- **03_async_usage.py** — асинхронное использование
- **04_retry_decorator.py** — использование retry декоратора
- **05_address_info_methods.py** — методы AddressInfo
- **06_search_methods.py** — методы поиска
- **07_location_methods.py** — определение локации по IP
- **08_error_handling.py** — обработка ошибок

## Тестирование

```bash
# Установка зависимостей для разработки
pip install -e ".[dev]"

# Запуск всех тестов
pytest

# Запуск с подробным выводом
pytest -vv

# Запуск конкретного теста
pytest tests/test_sync.py::TestSyncFPA::test_get_regions
```

## Лицензия

MIT. Подробности см. в файле [LICENSE](LICENSE).

## Полезные ссылки

- [PyPI Package](https://pypi.org/project/fias-public-api/)
- [Официальный сайт ФИАС](https://fias.nalog.ru/)
- [Swagger UI FIAS Public Service](https://fias-public-service.nalog.ru/api/spas/v2.0/swagger/index.html)

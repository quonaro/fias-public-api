# 🏠 FIAS Public API Python Client

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/fias-public-api.svg)](https://pypi.org/project/fias-public-api/)
[![PyPI downloads](https://img.shields.io/pypi/dm/fias-public-api.svg)](https://pypi.org/project/fias-public-api/)

> 🚀 **Простой и удобный Python клиент для работы с публичным API ФИАС (Федеральная информационная адресная система)**

## ✨ Возможности

| Возможность                | Описание                                              | Статус |
| -------------------------- | ----------------------------------------------------- | ------ |
| 🔍 **Поиск адресов**       | Текстовый поиск адресов с поддержкой русского языка  | ✅     |
| 📋 **Детали объектов**     | Получение полной информации об адресных объектах     | ✅     |
| 🔐 **Управление токенами** | Автоматическое получение токена аутентификации       | ✅     |
| ⚡ **Поддержка async**     | Синхронные и асинхронные операции                    | ✅     |
| 🔄 **Опциональный retry** | Декоратор для повторных попыток при ошибках (по желанию) | ✅     |

## 📚 Реализованные разделы API

Библиотека реализует методы из следующих разделов FIAS Public API:

- **AddressInfo** - Работа с адресными объектами (получение регионов, поиск по различным критериям, проверка иерархии)
- **Search** - Поиск адресов по текстовым строкам и получение подсказок
- **Location** - Определение населенного пункта по IP адресу

**Источник API спецификации:** [Swagger UI FIAS Public Service](https://fias-public-service.nalog.ru/api/spas/v2.0/swagger/index.html)

> ⚠️ **Важно:** Первый запрос к API ФИАС часто возвращает 500 ошибку или ConnectionResetError. 
> Для обработки таких ситуаций библиотека предоставляет опциональный декоратор `retry_on_error`, 
> который можно использовать для автоматических повторных попыток.

## 📊 Статистика проекта

![GitHub stars](https://img.shields.io/github/stars/quonaro/fias-public-api?style=social)
![GitHub forks](https://img.shields.io/github/forks/quonaro/fias-public-api?style=social)
![GitHub issues](https://img.shields.io/github/issues/quonaro/fias-public-api)
![GitHub pull requests](https://img.shields.io/github/issues-pr/quonaro/fias-public-api)

## 🚀 Быстрый старт

### Минимальный пример

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
    # Получаем токен автоматически
    token = await get_token_async()
    
    # Создаем асинхронный клиент
    async with AsyncFPA(token) as api:
        # Ищем адрес
        results = await api.search("Москва, Красная площадь")
        print(f"Найдено: {len(results)} результатов")
        
        # Получаем детали первого результата
        if results:
            details = await api.details_by_id(results[0]['id'])
            print(f"Адрес: {details.get('address', 'N/A')}")

asyncio.run(main())
```

## 📦 Установка

### Установка из PyPI (рекомендуется)

Установите пакет из [PyPI](https://pypi.org/project/fias-public-api/):

```bash
pip install fias-public-api
```

### Установка из GitHub

```bash
pip install git+https://github.com/quonaro/fias-public-api
```

### Зависимости

| Пакет      | Версия     | Описание                              |
| ---------- | ---------- | ------------------------------------- |
| `requests` | `>=2.32.5` | HTTP библиотека для API запросов      |
| `httpx`    | `>=0.28.1` | Асинхронная HTTP библиотека           |

## 🔧 Использование

### Базовые сценарии

#### 1. Поиск адресов

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
    print("---")
```

#### 2. Получение деталей объекта

```python
from fias_public_api import AddressType

# Получаем детали по ID
object_id = 12345
details = api.details_by_id(object_id, address_type=AddressType.MUNICIPALITY)

# Получаем детали по GUID
object_guid = "some-guid-string"
details = api.details_by_guid(object_guid, address_type=AddressType.ADMINISTRATIVE)

# Анализируем структуру ответа
print("Доступные поля:")
for key, value in details.items():
    if isinstance(value, (str, int, float, bool)) and value:
        print(f"  {key}: {value}")
```

#### 3. Обработка ошибок

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
except Exception as e:
    print(f"Неизвестная ошибка: {e}")
```

## 📚 Справочник API

### Синхронные классы

#### `SyncFPA`

Основной класс клиента для синхронных операций с FIAS Public API.

##### Конструктор

```python
SyncFPA(token: str, address_type: int | AddressType = 2)
```

**Параметры:**
- `token` (str) - Токен аутентификации для доступа к API
- `address_type` (int | AddressType, optional) - Тип адреса по умолчанию (по умолчанию 2 - MUNICIPALITY)

##### Методы

###### `search(search_string: str, url: str = "https://fias-public-service.nalog.ru/api/spas/v2.0/GetAddressHint") -> List[Dict]`

Поиск адресов по текстовой строке.

**Параметры:**
- `search_string` (str) - Текст для поиска (адрес, улица, город и т.д.)
- `url` (str, optional) - URL конечной точки API для поиска (по умолчанию используется стандартный endpoint)

**Возвращает:** Список найденных адресов в виде словарей

**Пример ответа:**

```json
[
  {
    "id": 12345,
    "address": "г Москва, Красная площадь",
    "type": "город",
    "level": 1
  }
]
```

###### `details_by_id(object_id: int, address_type: int | AddressType = 2) -> Dict`

Получить детальную информацию об адресном объекте по его ID.

**Параметры:**
- `object_id` (int) - ID объекта ФИАС
- `address_type` (int | AddressType) - Тип адреса (по умолчанию 2 - MUNICIPALITY)

**Возвращает:** Словарь с детальной информацией об объекте

###### `details_by_guid(object_guid: str, address_type: int | AddressType = 2) -> Dict`

Получить детальную информацию об адресном объекте по его GUID.

**Параметры:**
- `object_guid` (str) - GUID объекта ФИАС
- `address_type` (int | AddressType) - Тип адреса (по умолчанию 2 - MUNICIPALITY)

**Возвращает:** Словарь с детальной информацией об объекте

###### `get_regions() -> Dict`

Получить список регионов.

**Возвращает:** Словарь со списком регионов

###### `get_address_items(path: str | None = None, address_level: int | None = None, address_levels: list[int] | None = None, name_part: str | None = None, address_type: int | AddressType | None = None, include_descendants: bool | None = None) -> Dict`

Получить список дочерних элементов, соответствующих заданным фильтрам.

**Параметры:**
- `path` (str, optional) - Путь к родительскому элементу
- `address_level` (int, optional) - Уровень адреса
- `address_levels` (list[int], optional) - Список уровней адресов
- `name_part` (str, optional) - Часть названия для поиска
- `address_type` (int | AddressType, optional) - Тип адреса
- `include_descendants` (bool, optional) - Включать ли дочерние элементы

**Возвращает:** Словарь со списком адресных элементов

###### `get_details(object_id: int) -> Dict`

Получить дополнительную информацию для заданного адресного элемента.

**Параметры:**
- `object_id` (int) - Идентификатор адресного элемента

**Возвращает:** Словарь с дополнительной информацией

###### `is_descendant(ancestor: int, descendant: int, address_type: int | AddressType | None = None) -> Dict`

Проверка, является ли элемент ancestor родительским элементом в иерархии для элемента descendant.

**Параметры:**
- `ancestor` (int) - Идентификатор родительского элемента
- `descendant` (int) - Идентификатор дочернего элемента
- `address_type` (int | AddressType, optional) - Вид представления адреса

**Возвращает:** Словарь с результатом проверки

###### `has_descendants(parent: int, up_to_level: int, address_type: int | AddressType | None = None) -> Dict`

Проверка, имеет ли элемент parent дочерние элементы до уровня up_to_level.

**Параметры:**
- `parent` (int) - Идентификатор родительского элемента
- `up_to_level` (int) - Максимальный уровень дочерних элементов
- `address_type` (int | AddressType, optional) - Вид представления адреса

**Возвращает:** Словарь с результатом проверки

###### `get_address_item_by_cadastral_number(cadastral_number: str, address_type: int | AddressType | None = None) -> Dict`

Получение адресного элемента по кадастровому номеру.

**Параметры:**
- `cadastral_number` (str) - Кадастровый номер
- `address_type` (int | AddressType, optional) - Тип адреса

**Возвращает:** Словарь с адресным элементом

###### `get_fias_object_types() -> Dict`

Получение типов объектов ФИАС.

**Возвращает:** Словарь со списком типов объектов ФИАС

###### `search_address_items(search_string: str, address_type: int | AddressType | None = None) -> Dict`

Получение адресных элементов, соответствующих заданной произвольной строке адреса.

**Параметры:**
- `search_string` (str) - Адрес строкой
- `address_type` (int | AddressType, optional) - Вид представления адреса

**Возвращает:** Словарь со списком адресных элементов

###### `get_address_hint(search_string: str | None = None, address_type: int | AddressType | None = None, up_to_level: int | None = None, locations_boost: int | None = None, search_non_active: bool = False) -> Dict`

Сервис для организации стандартизированного ввода и поиска адреса (унифицированная адресная строка).

**Параметры:**
- `search_string` (str, optional) - Адрес строкой (для GET запроса)
- `address_type` (int | AddressType, optional) - Вид представления адреса
- `up_to_level` (int, optional) - Максимальный уровень поиска
- `locations_boost` (int, optional) - Приоритет локаций
- `search_non_active` (bool) - Искать неактивные адреса

**Возвращает:** Словарь со списком подсказок адресов

###### `search_address_item(search_string: str, address_type: int | AddressType | None = None) -> Dict`

Получение адресного элемента, соответствующего заданной произвольной строке адреса.

**Параметры:**
- `search_string` (str) - Адрес строкой
- `address_type` (int | AddressType, optional) - Вид представления адреса

**Возвращает:** Словарь с адресным элементом

###### `get_location_by_ip(ip: str, address_type: int | AddressType | None = None) -> Dict`

Получение населённого пункта по IP адресу.

**Параметры:**
- `ip` (str) - IP адрес
- `address_type` (int | AddressType, optional) - Тип представления возвращаемых адресных объектов

**Возвращает:** Словарь с адресными объектами

### Асинхронные классы

#### `AsyncFPA`

Основной класс клиента для асинхронных операций с FIAS Public API.

##### Конструктор

```python
AsyncFPA(token: str, address_type: int | AddressType = 2)
```

**Параметры:**
- `token` (str) - Токен аутентификации для доступа к API
- `address_type` (int | AddressType, optional) - Тип адреса по умолчанию (по умолчанию 2 - MUNICIPALITY)

##### Контекстный менеджер

```python
async with AsyncFPA(token) as api:
    results = await api.search("Москва")
```

##### Методы

Все методы из `SyncFPA` доступны в асинхронной версии с поддержкой `async`/`await`:
- `async get_regions() -> Dict`
- `async get_address_items(...) -> Dict`
- `async get_details(object_id: int) -> Dict`
- `async is_descendant(ancestor: int, descendant: int, ...) -> Dict`
- `async has_descendants(parent: int, up_to_level: int, ...) -> Dict`
- `async details_by_id(object_id: int, ...) -> Dict`
- `async details_by_guid(object_guid: str, ...) -> Dict`
- `async get_address_item_by_cadastral_number(cadastral_number: str, ...) -> Dict`
- `async get_fias_object_types() -> Dict`
- `async search_address_items(search_string: str, ...) -> Dict`
- `async get_address_hint(...) -> Dict`
- `async search_address_item(search_string: str, ...) -> Dict`
- `async get_location_by_ip(ip: str, ...) -> Dict`
- `async search(search_string: str, ...) -> List[Dict]`

### Функции

#### `get_token_sync(url: str = "https://fias.nalog.ru/") -> str`

Получить токен аутентификации из сервиса ФИАС (синхронно).

**Параметры:**
- `url` (str) - Базовый URL сервиса ФИАС

**Возвращает:** Строка с токеном аутентификации

**Исключения:**
- `ValueError` - Если не удалось получить токен
- `requests.HTTPError` - Если HTTP запрос завершился ошибкой

#### `get_token_async(url: str = "https://fias.nalog.ru/") -> str`

Получить токен аутентификации из сервиса ФИАС (асинхронно).

**Параметры:**
- `url` (str) - Базовый URL сервиса ФИАС

**Возвращает:** Строка с токеном аутентификации

**Исключения:**
- `ValueError` - Если не удалось получить токен
- `httpx.HTTPError` - Если HTTP запрос завершился ошибкой

#### `STANDART_HEADERS(token: str) -> Dict[str, str]`

Создать стандартные заголовки для HTTP запросов.

**Параметры:**
- `token` (str) - Токен аутентификации

**Возвращает:** Словарь с заголовками для HTTP запросов

#### `AddressType` (Enum)

Перечисление типов адресов в системе ФИАС.

**Значения:**
- `AddressType.ADMINISTRATIVE = 1` - Административный тип
- `AddressType.MUNICIPALITY = 2` - Муниципальный тип (по умолчанию)

#### `retry_on_error(max_retries: int = 3, delay: float = 0.5, backoff: float = 2.0, exceptions: tuple | None = None)`

Декоратор для автоматических повторных попыток при ошибках.

**Параметры:**
- `max_retries` (int) - Максимальное количество попыток (по умолчанию 3)
- `delay` (float) - Начальная задержка между попытками в секундах (по умолчанию 0.5)
- `backoff` (float) - Множитель для увеличения задержки (по умолчанию 2.0)
- `exceptions` (tuple | None) - Кортеж исключений, при которых нужно повторять попытку (по умолчанию все исключения)

**Пример использования:**

```python
from fias_public_api import SyncFPA, get_token_sync, retry_on_error
from requests.exceptions import ConnectionError, HTTPError

token = get_token_sync()
api = SyncFPA(token)

# Применяем декоратор к функции
@retry_on_error(
    max_retries=5,
    delay=1.0,
    backoff=2.0,
    exceptions=(ConnectionError, HTTPError)
)
def search_with_retry(search_string):
    return api.search_address_items(search_string)

# Использование
results = search_with_retry("Москва")
```

## 📖 Примеры использования

Все примеры доступны в папке [`examples/`](examples/). Вот краткий обзор:

- **01_basic_usage.py** - Базовое использование API
- **02_address_types.py** - Работа с типами адресов
- **03_async_usage.py** - Асинхронное использование
- **04_retry_decorator.py** - Использование retry декоратора
- **05_address_info_methods.py** - Методы AddressInfo
- **06_search_methods.py** - Методы поиска
- **07_location_methods.py** - Определение локации по IP
- **08_error_handling.py** - Обработка ошибок

Подробнее см. [examples/README.md](examples/README.md)

## 💡 Дополнительные примеры

### Пример 1: Поиск улиц в городе

```python
def find_streets_in_city(city_name: str, street_pattern: str = ""):
    """Найти улицы в указанном городе"""
    api = SyncFPA(get_token_sync())

    # Ищем город
    cities = api.search(city_name)
    if not cities:
        print(f"Город '{city_name}' не найден")
        return

    city = cities[0]
    print(f"Найден город: {city['address']}")

    # Ищем улицы
    search_query = f"{city_name}, {street_pattern}" if street_pattern else city_name
    streets = api.search(search_query)

    print(f"\nНайдено улиц: {len(streets)}")
    for street in streets[:10]:  # Показываем первые 10
        print(f"  - {street.get('address', 'N/A')}")

# Использование
find_streets_in_city("Москва", "Тверская")
```

### Пример 2: Получение иерархии адреса

```python
def get_address_hierarchy(address_id: int):
    """Получить полную иерархию адреса"""
    api = SyncFPA(get_token_sync())

    try:
        details = api.details_by_id(address_id)

        print("🏠 Иерархия адреса:")
        print(f"  Уровень: {details.get('level', 'N/A')}")
        print(f"  Тип: {details.get('type', 'N/A')}")
        print(f"  Название: {details.get('name', 'N/A')}")
        print(f"  Полный адрес: {details.get('address', 'N/A')}")

        # Дополнительная информация
        if 'coordinates' in details:
            coords = details['coordinates']
            print(f"  Координаты: {coords.get('lat', 'N/A')}, {coords.get('lon', 'N/A')}")

    except Exception as e:
        print(f"❌ Ошибка при получении деталей: {e}")

# Использование
get_address_hierarchy(12345)
```

### Пример 3: Пакетный поиск адресов (Async)

```python
import asyncio
from typing import List, Dict

async def batch_address_search_async(queries: List[str], delay: float = 0.1) -> Dict[str, List]:
    """Пакетный поиск адресов с задержкой между запросами"""
    token = await get_token_async()
    
    async with AsyncFPA(token) as api:
        results = {}
        
        print(f"🔍 Начинаем поиск для {len(queries)} адресов...")
        
        for i, query in enumerate(queries, 1):
            try:
                print(f"  [{i}/{len(queries)}] Ищем: {query}")
                search_results = await api.search(query)
                results[query] = search_results
                print(f"     Найдено: {len(search_results)} результатов")
                
                # Задержка между запросами
                if i < len(queries):
                    await asyncio.sleep(delay)
                    
            except Exception as e:
                print(f"     ❌ Ошибка: {e}")
                results[query] = []
        
        return results

# Использование
addresses_to_search = [
    "Москва, Красная площадь",
    "Санкт-Петербург, Дворцовая площадь",
    "Казань, Кремль",
    "Новосибирск, Красный проспект"
]

results = asyncio.run(batch_address_search_async(addresses_to_search, delay=0.2))
```

### Пример 4: Параллельные асинхронные операции

```python
import asyncio
from typing import List

async def concurrent_address_search(addresses: List[str]) -> List[Dict]:
    """Поиск нескольких адресов параллельно"""
    token = await get_token_async()
    
    async with AsyncFPA(token) as api:
        # Создаем задачи для параллельного выполнения
        tasks = [api.search(address) for address in addresses]
        
        # Выполняем все поиски параллельно
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Обрабатываем результаты
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Ошибка при поиске '{addresses[i]}': {result}")
                processed_results.append([])
            else:
                processed_results.append(result)
        
        return processed_results

# Использование
addresses = ["Москва", "Санкт-Петербург", "Казань", "Новосибирск"]
results = asyncio.run(concurrent_address_search(addresses))
```

## 🧪 Тестирование

Для запуска тестов используйте pytest:

```bash
# Установите зависимости для разработки
pip install -e ".[dev]"

# Запустите все тесты (с подробным выводом)
pytest

# Запустите тесты с максимально подробным выводом
pytest -vv

# Запустите тесты с полным traceback (как в Python интерпретаторе)
pytest --tb=long

# Запустите тесты с показом локальных переменных при ошибках
pytest --showlocals

# Запустите конкретный тестовый файл
pytest tests/test_sync.py

# Запустите конкретный тест
pytest tests/test_sync.py::TestSyncFPA::test_get_regions

# Запустите тесты с выводом print statements
pytest -s

# Запустите тесты и покажите 10 самых медленных
pytest --durations=10
```

### Настройка вывода pytest

Pytest настроен для вывода, похожего на Python интерпретатор:
- `-vv` - подробный вывод (включен по умолчанию)
- `--tb=short` - короткий traceback (включен по умолчанию)
- `--showlocals` - показ локальных переменных при ошибках (включен по умолчанию)
- `--color=yes` - цветной вывод (включен по умолчанию)

Все эти настройки находятся в `pyproject.toml` в секции `[tool.pytest.ini_options]`.

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности см. в файле [LICENSE](LICENSE).

## 🔗 Полезные ссылки

- [📦 PyPI Package](https://pypi.org/project/fias-public-api/) - Установка через PyPI
- [🌐 Официальный сайт ФИАС](https://fias.nalog.ru/)
- [📖 Swagger UI FIAS Public Service](https://fias-public-service.nalog.ru/api/spas/v2.0/swagger/index.html) - API документация

---

<div align="center">

**Сделано с ❤️**

[![GitHub](https://img.shields.io/badge/GitHub-quonaro-black?style=flat-square&logo=github)](https://github.com/quonaro)

</div>

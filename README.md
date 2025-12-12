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

**Примечание:** Метод `details()` устарел и будет удален в будущих версиях. Используйте `details_by_id()` или `details_by_guid()`.

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
SyncFPA(token: str)
```

**Параметры:**
- `token` (str) - Токен аутентификации для доступа к API

##### Методы

###### `search(search_string: str, url: str = None) -> List[Dict]`

Поиск адресов по текстовой строке.

**Параметры:**
- `search_string` (str) - Текст для поиска (адрес, улица, город и т.д.)
- `url` (str, optional) - Кастомный URL конечной точки API

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

###### `details(object_id: int, address_type: int | AddressType = 2) -> Dict` ⚠️ Устарело

**Устаревший метод.** Используйте `details_by_id()` вместо этого. Будет удален в будущих версиях.

### Асинхронные классы

#### `AsyncFPA`

Основной класс клиента для асинхронных операций с FIAS Public API.

##### Конструктор

```python
AsyncFPA(token: str)
```

**Параметры:**
- `token` (str) - Токен аутентификации для доступа к API

##### Контекстный менеджер

```python
async with AsyncFPA(token) as api:
    results = await api.search("Москва")
```

##### Методы

Те же методы, что и у `SyncFPA`, но с поддержкой `async`/`await`:
- `async search(search_string: str, url: str = None) -> List[Dict]`
- `async details_by_id(object_id: int, address_type: int | AddressType = 2) -> Dict`
- `async details_by_guid(object_guid: str, address_type: int | AddressType = 2) -> Dict`
- `async details(object_id: int, address_type: int | AddressType = 2) -> Dict` ⚠️ Устарело

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

## 💡 Примеры

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

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. Подробности см. в файле [LICENSE](LICENSE).

## 🔗 Полезные ссылки

- [📦 PyPI Package](https://pypi.org/project/fias-public-api/) - Установка через PyPI
- [🌐 Официальный сайт ФИАС](https://fias.nalog.ru/)

---

<div align="center">

**Сделано с ❤️**

[![GitHub](https://img.shields.io/badge/GitHub-quonaro-black?style=flat-square&logo=github)](https://github.com/quonaro)

</div>

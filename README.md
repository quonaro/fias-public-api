# 🏠 FIAS Public API Python Client

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/PyPI-Not%20Published-red.svg)](https://pypi.org/project/fias-public-api/)

> 🚀 **Simple and convenient Python client for working with the Russian FIAS (Federal Information Address System) Public API**

## ✨ Features

| Feature                | Description                                              | Status |
| ---------------------- | -------------------------------------------------------- | ------ |
| 🔍 **Address Search**  | Text-based address search with Russian language support | ✅     |
| 📋 **Object Details**  | Get complete information about address objects           | ✅     |
| 🔐 **Token Management**| Automatic authentication token retrieval                | ✅     |
| ⚡ **Async Support**   | Both synchronous and asynchronous operations            | ✅     |

## 📊 Project Statistics

![GitHub stars](https://img.shields.io/github/stars/invoxy/fias-public-api?style=social)
![GitHub forks](https://img.shields.io/github/forks/invoxy/fias-public-api?style=social)
![GitHub issues](https://img.shields.io/github/issues/invoxy/fias-public-api)
![GitHub pull requests](https://img.shields.io/github/issues-pr/invoxy/fias-public-api)

## 🚀 Quick Start

### Minimal Example

```python
from fias_public_api import get_token_sync, SyncFPA

# Get token automatically
token = get_token_sync()

# Create client
api = SyncFPA(token)

# Search for address
results = api.search("Moscow, Red Square")
print(f"Found: {len(results)} results")

# Get details of first result
if results:
    details = api.details(results[0]['id'])
    print(f"Address: {details.get('address', 'N/A')}")
```

### Async Example

```python
import asyncio
from fias_public_api import get_token_async, AsyncFPA

async def main():
    # Get token automatically
    token = await get_token_async()
    
    # Create async client
    async with AsyncFPA(token) as api:
        # Search for address
        results = await api.search("Moscow, Red Square")
        print(f"Found: {len(results)} results")
        
        # Get details of first result
        if results:
            details = await api.details(results[0]['id'])
            print(f"Address: {details.get('address', 'N/A')}")

asyncio.run(main())
```

## 📦 Installation

```bash
pip install git+https://github.com/invoxy/fias-public-api
```

### Dependencies

| Package     | Version     | Description                         |
| ----------- | ----------- | ----------------------------------- |
| `requests`  | `>=2.32.5`  | HTTP library for API requests       |
| `httpx`     | `>=0.25.0`  | Async HTTP library for async operations |

## 🔧 Usage

### Basic Scenarios

#### 1. Address Search

```python
# Simple search
results = api.search("Moscow")

# Search with custom URL
results = api.search("Saint Petersburg", url="https://custom-fias.ru/api")

# Process results
for result in results:
    print(f"ID: {result['id']}")
    print(f"Address: {result['address']}")
    print(f"Type: {result['type']}")
    print("---")
```

#### 2. Get Object Details

```python
# Get details by ID
object_id = 12345
details = api.details(object_id)

# Analyze response structure
print("Available fields:")
for key, value in details.items():
    if isinstance(value, (str, int, float, bool)) and value:
        print(f"  {key}: {value}")
```

#### 3. Error Handling

```python
from requests.exceptions import HTTPError, RequestException

try:
    results = api.search("Non-existent address")
except HTTPError as e:
    if e.response.status_code == 404:
        print("Address not found")
    elif e.response.status_code == 401:
        print("Invalid token")
    else:
        print(f"HTTP error: {e}")
except RequestException as e:
    print(f"Network error: {e}")
except Exception as e:
    print(f"Unknown error: {e}")
```

## 📚 API Reference

### Synchronous Classes

#### `SyncFPA`

Main client class for synchronous FIAS Public API operations.

##### Constructor

```python
SyncFPA(token: str)
```

**Parameters:**
- `token` (str) - Authentication token for API access

##### Methods

###### `search(search_string: str, url: str = None) -> List[Dict]`

Search for addresses by text string.

**Parameters:**
- `search_string` (str) - Text to search for (address, street, city, etc.)
- `url` (str, optional) - Custom API endpoint URL

**Returns:** List of found addresses as dictionaries

**Example response:**

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

###### `details(object_id: int) -> Dict`

Get detailed information about an address object.

**Parameters:**
- `object_id` (int) - FIAS object ID

**Returns:** Dictionary with detailed object information

### Asynchronous Classes

#### `AsyncFPA`

Main client class for asynchronous FIAS Public API operations.

##### Constructor

```python
AsyncFPA(token: str)
```

**Parameters:**
- `token` (str) - Authentication token for API access

##### Context Manager

```python
async with AsyncFPA(token) as api:
    results = await api.search("Moscow")
```

##### Methods

Same methods as `SyncFPA` but with `async`/`await` support:
- `async search(search_string: str, url: str = None) -> List[Dict]`
- `async details(object_id: int) -> Dict`

### Functions

#### `get_token_sync(url: str = "https://fias.nalog.ru/") -> str`

Get authentication token from FIAS service (synchronous).

**Parameters:**
- `url` (str) - Base URL for FIAS service

**Returns:** Authentication token string

**Exceptions:**
- `ValueError` - If token retrieval fails
- `requests.HTTPError` - If HTTP request fails

#### `get_token_async(url: str = "https://fias.nalog.ru/") -> str`

Get authentication token from FIAS service (asynchronous).

**Parameters:**
- `url` (str) - Base URL for FIAS service

**Returns:** Authentication token string

**Exceptions:**
- `ValueError` - If token retrieval fails
- `httpx.HTTPError` - If HTTP request fails

#### `STANDART_HEADERS(token: str) -> Dict[str, str]`

Generate standard headers for HTTP requests.

**Parameters:**
- `token` (str) - Authentication token

**Returns:** Dictionary with headers for HTTP requests

## 💡 Examples

### Example 1: Find Streets in a City

```python
def find_streets_in_city(city_name: str, street_pattern: str = ""):
    """Find streets in specified city"""
    api = SyncFPA(get_token_sync())

    # Search for city
    cities = api.search(city_name)
    if not cities:
        print(f"City '{city_name}' not found")
        return

    city = cities[0]
    print(f"Found city: {city['address']}")

    # Search for streets
    search_query = f"{city_name}, {street_pattern}" if street_pattern else city_name
    streets = api.search(search_query)

    print(f"\nFound streets: {len(streets)}")
    for street in streets[:10]:  # Show first 10
        print(f"  - {street.get('address', 'N/A')}")

# Usage
find_streets_in_city("Moscow", "Tverskaya")
```

### Example 2: Get Address Hierarchy

```python
def get_address_hierarchy(address_id: int):
    """Get complete address hierarchy"""
    api = SyncFPA(get_token_sync())

    try:
        details = api.details(address_id)

        print("🏠 Address hierarchy:")
        print(f"  Level: {details.get('level', 'N/A')}")
        print(f"  Type: {details.get('type', 'N/A')}")
        print(f"  Name: {details.get('name', 'N/A')}")
        print(f"  Full address: {details.get('address', 'N/A')}")

        # Additional information
        if 'coordinates' in details:
            coords = details['coordinates']
            print(f"  Coordinates: {coords.get('lat', 'N/A')}, {coords.get('lon', 'N/A')}")

    except Exception as e:
        print(f"❌ Error getting details: {e}")

# Usage
get_address_hierarchy(12345)
```

### Example 3: Batch Address Search (Async)

```python
import asyncio
from typing import List, Dict

async def batch_address_search_async(queries: List[str], delay: float = 0.1) -> Dict[str, List]:
    """Batch address search with delay between requests"""
    token = await get_token_async()
    
    async with AsyncFPA(token) as api:
        results = {}
        
        print(f"🔍 Starting search for {len(queries)} addresses...")
        
        for i, query in enumerate(queries, 1):
            try:
                print(f"  [{i}/{len(queries)}] Searching: {query}")
                search_results = await api.search(query)
                results[query] = search_results
                print(f"     Found: {len(search_results)} results")
                
                # Delay between requests
                if i < len(queries):
                    await asyncio.sleep(delay)
                    
            except Exception as e:
                print(f"     ❌ Error: {e}")
                results[query] = []
        
        return results

# Usage
addresses_to_search = [
    "Moscow, Red Square",
    "Saint Petersburg, Palace Square",
    "Kazan, Kremlin",
    "Novosibirsk, Red Avenue"
]

results = asyncio.run(batch_address_search_async(addresses_to_search, delay=0.2))
```

### Example 4: Concurrent Async Operations

```python
import asyncio
from typing import List

async def concurrent_address_search(addresses: List[str]) -> List[Dict]:
    """Search multiple addresses concurrently"""
    token = await get_token_async()
    
    async with AsyncFPA(token) as api:
        # Create tasks for concurrent execution
        tasks = [api.search(address) for address in addresses]
        
        # Execute all searches concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"Error searching '{addresses[i]}': {result}")
                processed_results.append([])
            else:
                processed_results.append(result)
        
        return processed_results

# Usage
addresses = ["Moscow", "Saint Petersburg", "Kazan", "Novosibirsk"]
results = asyncio.run(concurrent_address_search(addresses))
```

## 📄 License

This project is distributed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🔗 Useful Links

- [🌐 Official FIAS Website](https://fias.nalog.ru/)

---

<div align="center">

**Made with ❤️**

[![GitHub](https://img.shields.io/badge/GitHub-quonaro-black?style=flat-square&logo=github)](https://github.com/quonaro)

</div>
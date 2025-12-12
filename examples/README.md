# Examples

This directory contains various examples demonstrating how to use the FIAS Public API client.

## Examples List

### 01_basic_usage.py
Basic usage example showing:
- Getting authentication token
- Creating API client
- Searching for addresses
- Getting address details

**Run:**
```bash
python examples/01_basic_usage.py
```

### 02_address_types.py
Demonstrates AddressType usage:
- Administrative division (ADMINISTRATIVE)
- Municipal division (MUNICIPALITY)
- Overriding address type for specific requests

**Run:**
```bash
python examples/02_address_types.py
```

### 03_async_usage.py
Asynchronous usage example:
- Async token retrieval
- Async client with context manager
- Concurrent requests

**Run:**
```bash
python examples/03_async_usage.py
```

### 04_retry_decorator.py
Shows how to use `retry_on_error` decorator:
- Applying retry to functions
- Custom retry parameters
- Handling connection errors

**Run:**
```bash
python examples/04_retry_decorator.py
```

### 05_address_info_methods.py
Demonstrates AddressInfo methods:
- Getting regions
- Getting address items with filters
- Getting address details
- Checking hierarchy relationships

**Run:**
```bash
python examples/05_address_info_methods.py
```

### 06_search_methods.py
Shows different search operations:
- SearchAddressItems
- GetAddressHint (GET and POST)
- SearchAddressItem

**Run:**
```bash
python examples/06_search_methods.py
```

### 07_location_methods.py
Demonstrates Location methods:
- Getting location by IP address
- Using different address types

**Run:**
```bash
python examples/07_location_methods.py
```

### 08_error_handling.py
Error handling examples:
- Basic error handling
- Using retry decorator
- Handling specific error codes
- Wrapping multiple operations

**Run:**
```bash
python examples/08_error_handling.py
```

## Requirements

All examples require:
- Python 3.12+
- `fias-public-api` package installed
- Internet connection for API requests

## Notes

- Some examples may fail if the API is unavailable or returns errors
- First request to FIAS API often returns 500 error - use retry decorator for production code
- Replace example IP addresses and addresses with real values for testing


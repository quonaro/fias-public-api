"""
Example demonstrating error handling.

This example shows how to handle various errors:
- Connection errors
- HTTP errors
- Invalid requests
- Using retry decorator
"""

from fias_public_api import get_token_sync, SyncFPA, retry_on_error
from requests.exceptions import ConnectionError, HTTPError, RequestException


def main():
    print("⚠️ Error Handling Examples\n")

    # Example 1: Basic error handling
    print("1️⃣ Basic error handling...")
    try:
        token = get_token_sync()
        api = SyncFPA(token)
        
        # This might fail if address doesn't exist
        results = api.search_address_items("NonExistentAddress12345")
        print("✅ Request successful")
    except HTTPError as e:
        if e.response.status_code == 404:
            print("❌ Address not found (404)")
        elif e.response.status_code == 500:
            print("❌ Server error (500) - this often happens on first request")
        else:
            print(f"❌ HTTP error: {e.response.status_code}")
    except ConnectionError as e:
        print(f"❌ Connection error: {e}")
    except RequestException as e:
        print(f"❌ Request error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    # Example 2: Using retry decorator
    print("\n2️⃣ Using retry decorator for error handling...")
    
    @retry_on_error(max_retries=3, delay=0.5)
    def safe_search(api: SyncFPA, query: str):
        """Search with automatic retry on errors."""
        return api.search_address_items(query)
    
    try:
        token = get_token_sync()
        api = SyncFPA(token)
        
        results = safe_search(api, "Москва")
        print(f"✅ Search successful: {len(results.get('addresses', []))} results")
    except Exception as e:
        print(f"❌ Failed after retries: {e}")

    # Example 3: Handling specific error codes
    print("\n3️⃣ Handling specific error codes...")
    try:
        token = get_token_sync()
        api = SyncFPA(token)
        
        # Try to get details for invalid ID
        details = api.details_by_id(object_id=999999999)
        print("✅ Details retrieved")
    except HTTPError as e:
        status_code = e.response.status_code
        if status_code == 404:
            print("❌ Object not found (404)")
        elif status_code == 401:
            print("❌ Unauthorized - check your token (401)")
        elif status_code == 500:
            print("❌ Server error (500)")
        else:
            print(f"❌ HTTP error: {status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Example 4: Wrapping multiple operations
    print("\n4️⃣ Wrapping multiple operations with error handling...")
    
    def safe_operations(api: SyncFPA):
        """Perform multiple operations with error handling."""
        results = []
        
        # Operation 1: Get regions
        try:
            regions = api.get_regions()
            results.append(("Get regions", "✅ Success"))
        except Exception as e:
            results.append(("Get regions", f"❌ Error: {e}"))
        
        # Operation 2: Search
        try:
            search_results = api.search("Москва")
            results.append(("Search", f"✅ Found {len(search_results)} results"))
        except Exception as e:
            results.append(("Search", f"❌ Error: {e}"))
        
        # Operation 3: Get types
        try:
            types = api.get_fias_object_types()
            type_count = len(types.get('types', []))
            results.append(("Get types", f"✅ Found {type_count} types"))
        except Exception as e:
            results.append(("Get types", f"❌ Error: {e}"))
        
        return results
    
    try:
        token = get_token_sync()
        api = SyncFPA(token)
        
        results = safe_operations(api)
        print("\n📋 Operation results:")
        for operation, status in results:
            print(f"   {operation}: {status}")
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")


if __name__ == "__main__":
    main()


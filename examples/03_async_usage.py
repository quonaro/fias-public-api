"""
Asynchronous usage example for FIAS Public API.

This example demonstrates:
- Async token retrieval
- Async client usage
- Concurrent requests
"""

import asyncio
from fias_public_api import get_token_async, AsyncFPA


async def search_address(api: AsyncFPA, query: str):
    """Search for an address asynchronously."""
    results = await api.search(query)
    return {
        "query": query,
        "count": len(results),
        "results": results[:3]  # First 3 results
    }


async def main():
    # Step 1: Get authentication token
    print("🔑 Getting authentication token...")
    token = await get_token_async()
    print(f"✅ Token received: {token[:20]}...")

    # Step 2: Create async API client using context manager
    print("\n📦 Creating async API client...")
    async with AsyncFPA(token) as api:
        print("✅ Client created")

        # Step 3: Single async request
        print("\n🔍 Single async search...")
        results = await api.search("Москва")
        print(f"✅ Found {len(results)} results")

        # Step 4: Concurrent requests
        print("\n🔍 Performing concurrent searches...")
        queries = [
            "Москва",
            "Санкт-Петербург",
            "Казань",
            "Новосибирск"
        ]

        tasks = [search_address(api, query) for query in queries]
        results = await asyncio.gather(*tasks)

        print("\n📋 Concurrent search results:")
        for result in results:
            print(f"  {result['query']}: {result['count']} results")
            if result['results']:
                print(f"    First result: {result['results'][0].get('full_name', 'N/A')}")


if __name__ == "__main__":
    asyncio.run(main())


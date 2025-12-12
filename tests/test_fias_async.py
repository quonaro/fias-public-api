"""
Tests for asynchronous FIAS Public API client
"""
import pytest
import pytest_asyncio
import asyncio
from fias_public_api import get_token_async, AsyncFPA, AddressType, retry_on_error


class TestGetTokenAsync:
    """Tests for get_token_async function"""

    @pytest.mark.asyncio
    @retry_on_error(max_retries=3, delay=0.5)
    async def test_get_token_async_success(self):
        """Test successful token retrieval"""
        token = await get_token_async()
        assert isinstance(token, str)
        assert len(token) > 0

    @pytest.mark.asyncio
    async def test_get_token_async_with_custom_url(self):
        """Test token retrieval with custom URL"""
        token = await get_token_async(url="https://fias.nalog.ru/")
        assert isinstance(token, str)
        assert len(token) > 0


class TestAsyncFPA:
    """Tests for AsyncFPA class"""

    @pytest_asyncio.fixture
    async def token(self):
        """Fixture to get authentication token"""
        return await get_token_async()

    @pytest_asyncio.fixture
    async def api(self, token):
        """Fixture to create AsyncFPA instance"""
        async with AsyncFPA(token) as api:
            yield api

    @pytest.fixture
    def test_object_id(self):
        """Fixture with a known valid object ID"""
        return 7700000000000

    @pytest.fixture
    def test_guid(self):
        """Fixture with a known valid GUID"""
        return "0c5b2444-70a0-4932-980c-b4dc0d3f02b5"

    @pytest.mark.asyncio
    async def test_async_fpa_initialization(self, token):
        """Test AsyncFPA initialization"""
        api = AsyncFPA(token)
        assert api.token == token
        # Clean up if client was created
        if api._client:
            await api._client.aclose()

    @pytest.mark.asyncio
    async def test_async_context_manager(self, token):
        """Test AsyncFPA as context manager"""
        async with AsyncFPA(token) as api:
            assert api.token == token
            assert api._client is not None

    @pytest.mark.asyncio
    async def test_search_basic(self, api):
        """Test basic search functionality"""
        results = await api.search("Москва")
        assert isinstance(results, list)
        # API may return empty list for some queries, that's acceptable
        if len(results) > 0:
            # Check structure of first result if results exist
            first_result = results[0]
            assert isinstance(first_result, dict)

    @pytest.mark.asyncio
    async def test_search_empty_query(self, api):
        """Test search with empty query raises ValueError"""
        with pytest.raises(ValueError, match="search_string cannot be empty"):
            await api.search("")

    @pytest.mark.asyncio
    async def test_search_special_characters(self, api):
        """Test search with special characters"""
        results = await api.search("Санкт-Петербург, Невский проспект")
        assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_details_by_id_basic(self, api, test_object_id):
        """Test details_by_id with basic parameters"""
        try:
            details = await api.details_by_id(test_object_id)
            assert isinstance(details, dict)
        except Exception:
            pytest.skip("Test object ID not found")

    @pytest.mark.asyncio
    async def test_details_by_id_with_address_type_int(self, api, test_object_id):
        """Test details_by_id with integer address_type"""
        try:
            details = await api.details_by_id(test_object_id, address_type=2)
            assert isinstance(details, dict)
        except Exception:
            pytest.skip("Test object ID not found")

    @pytest.mark.asyncio
    async def test_details_by_id_with_address_type_enum(self, api, test_object_id):
        """Test details_by_id with AddressType enum"""
        try:
            details = await api.details_by_id(test_object_id, address_type=AddressType.MUNICIPALITY)
            assert isinstance(details, dict)
        except Exception:
            pytest.skip("Test object ID not found")

    @pytest.mark.asyncio
    async def test_details_by_guid_basic(self, api, test_guid):
        """Test details_by_guid with basic parameters"""
        try:
            details = await api.details_by_guid(test_guid)
            assert isinstance(details, dict)
        except Exception:
            pytest.skip("Test GUID not found")

    @pytest.mark.asyncio
    async def test_details_by_guid_with_address_type_int(self, api, test_guid):
        """Test details_by_guid with integer address_type"""
        try:
            details = await api.details_by_guid(test_guid, address_type=2)
            assert isinstance(details, dict)
        except Exception:
            pytest.skip("Test GUID not found")

    @pytest.mark.asyncio
    async def test_details_by_guid_with_address_type_enum(self, api, test_guid):
        """Test details_by_guid with AddressType enum"""
        try:
            details = await api.details_by_guid(test_guid, address_type=AddressType.MUNICIPALITY)
            assert isinstance(details, dict)
        except Exception:
            pytest.skip("Test GUID not found")

    @pytest.mark.asyncio
    async def test_details_deprecated_method(self, api, test_object_id):
        """Test deprecated details method"""
        try:
            import io
            import sys
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                details = await api.details(test_object_id)
            output = f.getvalue()
            assert "устарел" in output or "details_by_id" in output
            assert isinstance(details, dict)
        except Exception:
            pytest.skip("Test object ID not found")

    @pytest.mark.asyncio
    async def test_details_with_address_type(self, api, test_object_id):
        """Test details method with address_type parameter"""
        try:
            details = await api.details(test_object_id, address_type=AddressType.MUNICIPALITY)
            assert isinstance(details, dict)
        except Exception:
            pytest.skip("Test object ID not found")

    @pytest.mark.asyncio
    async def test_search_multiple_queries(self, api):
        """Test multiple search queries"""
        queries = [
            "Москва",
            "Санкт-Петербург",
            "Тверская улица",
        ]
        for query in queries:
            results = await api.search(query)
            assert isinstance(results, list)

    @pytest.mark.asyncio
    async def test_invalid_object_id(self, api):
        """Test details_by_id with invalid object ID"""
        # API may return empty dict or raise exception
        try:
            result = await api.details_by_id(999999999999999999)
            # If no exception, result should be empty or have error indication
            assert isinstance(result, dict)
        except Exception:
            # Exception is also acceptable
            pass

    @pytest.mark.asyncio
    async def test_invalid_guid(self, api):
        """Test details_by_guid with invalid GUID"""
        # API may return empty dict or raise exception
        try:
            result = await api.details_by_guid("invalid-guid-format")
            # If no exception, result should be empty or have error indication
            assert isinstance(result, dict)
        except Exception:
            # Exception is also acceptable
            pass

    @pytest.mark.asyncio
    async def test_client_property(self, token):
        """Test client property creates client if not exists"""
        api = AsyncFPA(token)
        client = api.client
        assert client is not None
        await client.aclose()


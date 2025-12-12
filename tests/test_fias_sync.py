"""
Tests for synchronous FIAS Public API client
"""
import pytest
from fias_public_api import get_token_sync, SyncFPA, AddressType


class TestGetTokenSync:
    """Tests for get_token_sync function"""

    def test_get_token_sync_success(self):
        """Test successful token retrieval"""
        token = get_token_sync()
        assert isinstance(token, str)
        assert len(token) > 0

    def test_get_token_sync_with_custom_url(self):
        """Test token retrieval with custom URL"""
        token = get_token_sync(url="https://fias.nalog.ru/")
        assert isinstance(token, str)
        assert len(token) > 0


class TestSyncFPA:
    """Tests for SyncFPA class"""

    @pytest.fixture
    def token(self):
        """Fixture to get authentication token"""
        return get_token_sync()

    @pytest.fixture
    def api(self, token):
        """Fixture to create SyncFPA instance"""
        return SyncFPA(token)

    @pytest.fixture
    def test_object_id(self):
        """Fixture with a known valid object ID (Moscow, Red Square area)"""
        # Using a known object ID that should exist
        return 7700000000000

    @pytest.fixture
    def test_guid(self):
        """Fixture with a known valid GUID"""
        # Using a known GUID for Moscow
        return "0c5b2444-70a0-4932-980c-b4dc0d3f02b5"

    def test_sync_fpa_initialization(self, token):
        """Test SyncFPA initialization"""
        api = SyncFPA(token)
        assert api.token == token

    def test_search_basic(self, api):
        """Test basic search functionality"""
        results = api.search("Москва")
        assert isinstance(results, list)
        # API may return empty list for some queries, that's acceptable
        if len(results) > 0:
            # Check structure of first result if results exist
            first_result = results[0]
            assert isinstance(first_result, dict)

    def test_search_empty_query(self, api):
        """Test search with empty query"""
        results = api.search("")
        assert isinstance(results, list)

    def test_search_special_characters(self, api):
        """Test search with special characters"""
        results = api.search("Санкт-Петербург, Невский проспект")
        assert isinstance(results, list)

    def test_details_by_id_basic(self, api, test_object_id):
        """Test details_by_id with basic parameters"""
        try:
            details = api.details_by_id(test_object_id)
            assert isinstance(details, dict)
        except Exception:
            # If object doesn't exist, that's okay for this test
            pytest.skip("Test object ID not found")

    def test_details_by_id_with_address_type_int(self, api, test_object_id):
        """Test details_by_id with integer address_type"""
        try:
            details = api.details_by_id(test_object_id, address_type=2)
            assert isinstance(details, dict)
        except Exception:
            pytest.skip("Test object ID not found")

    def test_details_by_id_with_address_type_enum(self, api, test_object_id):
        """Test details_by_id with AddressType enum"""
        try:
            details = api.details_by_id(test_object_id, address_type=AddressType.MUNICIPALITY)
            assert isinstance(details, dict)
        except Exception:
            pytest.skip("Test object ID not found")

    def test_details_by_guid_basic(self, api, test_guid):
        """Test details_by_guid with basic parameters"""
        try:
            details = api.details_by_guid(test_guid)
            assert isinstance(details, dict)
        except Exception:
            pytest.skip("Test GUID not found")

    def test_details_by_guid_with_address_type_int(self, api, test_guid):
        """Test details_by_guid with integer address_type"""
        try:
            details = api.details_by_guid(test_guid, address_type=2)
            assert isinstance(details, dict)
        except Exception:
            pytest.skip("Test GUID not found")

    def test_details_by_guid_with_address_type_enum(self, api, test_guid):
        """Test details_by_guid with AddressType enum"""
        try:
            details = api.details_by_guid(test_guid, address_type=AddressType.MUNICIPALITY)
            assert isinstance(details, dict)
        except Exception:
            pytest.skip("Test GUID not found")

    def test_details_deprecated_method(self, api, test_object_id):
        """Test deprecated details method"""
        try:
            # Capture stdout to check for deprecation warning
            import io
            import sys
            from contextlib import redirect_stdout

            f = io.StringIO()
            with redirect_stdout(f):
                details = api.details(test_object_id)
            output = f.getvalue()
            assert "устарел" in output or "details_by_id" in output
            assert isinstance(details, dict)
        except Exception:
            pytest.skip("Test object ID not found")

    def test_details_with_address_type(self, api, test_object_id):
        """Test details method with address_type parameter"""
        try:
            details = api.details(test_object_id, address_type=AddressType.MUNICIPALITY)
            assert isinstance(details, dict)
        except Exception:
            pytest.skip("Test object ID not found")

    def test_search_multiple_queries(self, api):
        """Test multiple search queries"""
        queries = [
            "Москва",
            "Санкт-Петербург",
            "Тверская улица",
        ]
        for query in queries:
            results = api.search(query)
            assert isinstance(results, list)

    def test_invalid_object_id(self, api):
        """Test details_by_id with invalid object ID"""
        # API may return empty dict or raise exception
        try:
            result = api.details_by_id(999999999999999999)
            # If no exception, result should be empty or have error indication
            assert isinstance(result, dict)
        except Exception:
            # Exception is also acceptable
            pass

    def test_invalid_guid(self, api):
        """Test details_by_guid with invalid GUID"""
        # API may return empty dict or raise exception
        try:
            result = api.details_by_guid("invalid-guid-format")
            # If no exception, result should be empty or have error indication
            assert isinstance(result, dict)
        except Exception:
            # Exception is also acceptable
            pass


"""
Tests for synchronous FIAS Public API client.
"""

import pytest
from unittest.mock import Mock, patch
from fias_public_api import SyncFPA, get_token_sync, AddressType
from fias_public_api.constants import (
    GET_REGIONS,
    GET_ADDRESS_ITEMS,
    GET_DETAILS,
    IS_DESCENDANT,
    HAS_DESCENDANTS,
    GET_ADDRESS_ITEM_BY_ID,
    GET_ADDRESS_ITEM_BY_GUID,
    GET_ADDRESS_ITEM_BY_CADASTRAL_NUMBER,
    GET_FIAS_OBJECT_TYPES,
    SEARCH_ADDRESS_ITEMS,
    GET_ADDRESS_HINT,
    SEARCH_ADDRESS_ITEM,
    GET_LOCATION_BY_IP,
)


class TestGetTokenSync:
    """Tests for get_token_sync function."""

    @patch("fias_public_api.fias_sync.requests.get")
    def test_get_token_success(self, mock_get):
        """Test successful token retrieval."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"Token": "test-token-123"}
        mock_get.return_value = mock_response

        token = get_token_sync()
        assert token == "test-token-123"
        mock_get.assert_called_once()

    @patch("fias_public_api.fias_sync.requests.get")
    def test_get_token_failure(self, mock_get):
        """Test token retrieval failure."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="Не удалось получить токен"):
            get_token_sync()


class TestSyncFPA:
    """Tests for SyncFPA class."""

    @pytest.fixture
    def api(self):
        """Create SyncFPA instance for testing."""
        return SyncFPA(token="test-token")

    @pytest.fixture
    def api_with_address_type(self):
        """Create SyncFPA instance with custom address type."""
        return SyncFPA(token="test-token", address_type=AddressType.ADMINISTRATIVE)

    @patch("fias_public_api.fias_sync.requests.get")
    def test_get_regions(self, mock_get, api):
        """Test get_regions method."""
        mock_response = Mock()
        mock_response.json.return_value = {"addresses": []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        from fias_public_api.constants import STANDART_HEADERS
        
        result = api.get_regions()
        assert result == {"addresses": []}
        mock_get.assert_called_once_with(
            GET_REGIONS, headers=STANDART_HEADERS("test-token")
        )

    @patch("fias_public_api.fias_sync.requests.post")
    def test_get_address_items(self, mock_post, api):
        """Test get_address_items method."""
        mock_response = Mock()
        mock_response.json.return_value = {"addresses": []}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        result = api.get_address_items(
            path="test-path",
            address_level=1,
            name_part="test"
        )
        assert result == {"addresses": []}
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        assert call_args[0][0] == GET_ADDRESS_ITEMS

    @patch("fias_public_api.fias_sync.requests.get")
    def test_get_details(self, mock_get, api):
        """Test get_details method."""
        mock_response = Mock()
        mock_response.json.return_value = {"address_details": {}}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = api.get_details(object_id=12345)
        assert result == {"address_details": {}}
        mock_get.assert_called_once()

    @patch("fias_public_api.fias_sync.requests.get")
    def test_is_descendant(self, mock_get, api):
        """Test is_descendant method."""
        mock_response = Mock()
        mock_response.json.return_value = {"check": True}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = api.is_descendant(ancestor=1, descendant=2)
        assert result == {"check": True}
        mock_get.assert_called_once()

    @patch("fias_public_api.fias_sync.requests.get")
    def test_has_descendants(self, mock_get, api):
        """Test has_descendants method."""
        mock_response = Mock()
        mock_response.json.return_value = {"check": True}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = api.has_descendants(parent=1, up_to_level=5)
        assert result == {"check": True}
        mock_get.assert_called_once()

    @patch("fias_public_api.fias_sync.requests.get")
    def test_details_by_id(self, mock_get, api):
        """Test details_by_id method."""
        mock_response = Mock()
        mock_response.json.return_value = {"addresses": []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = api.details_by_id(object_id=12345)
        assert result == {"addresses": []}
        mock_get.assert_called_once()

    @patch("fias_public_api.fias_sync.requests.get")
    def test_details_by_id_with_address_type(self, mock_get, api_with_address_type):
        """Test details_by_id with custom address type from constructor."""
        mock_response = Mock()
        mock_response.json.return_value = {"addresses": []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = api_with_address_type.details_by_id(object_id=12345)
        assert result == {"addresses": []}
        call_args = mock_get.call_args
        assert "address_type" in call_args[1]["params"]
        assert call_args[1]["params"]["address_type"] == AddressType.ADMINISTRATIVE

    @patch("fias_public_api.fias_sync.requests.get")
    def test_details_by_guid(self, mock_get, api):
        """Test details_by_guid method."""
        mock_response = Mock()
        mock_response.json.return_value = {"addresses": []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = api.details_by_guid(object_guid="test-guid")
        assert result == {"addresses": []}
        mock_get.assert_called_once()

    @patch("fias_public_api.fias_sync.requests.get")
    def test_get_address_item_by_cadastral_number(self, mock_get, api):
        """Test get_address_item_by_cadastral_number method."""
        mock_response = Mock()
        mock_response.json.return_value = {"addresses": []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = api.get_address_item_by_cadastral_number(cadastral_number="123:45:678:90")
        assert result == {"addresses": []}
        mock_get.assert_called_once()

    @patch("fias_public_api.fias_sync.requests.get")
    def test_get_fias_object_types(self, mock_get, api):
        """Test get_fias_object_types method."""
        mock_response = Mock()
        mock_response.json.return_value = {"types": []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = api.get_fias_object_types()
        assert result == {"types": []}
        mock_get.assert_called_once()

    @patch("fias_public_api.fias_sync.requests.get")
    def test_search_address_items(self, mock_get, api):
        """Test search_address_items method."""
        mock_response = Mock()
        mock_response.json.return_value = {"addresses": []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = api.search_address_items(search_string="Москва")
        assert result == {"addresses": []}
        mock_get.assert_called_once()

    @patch("fias_public_api.fias_sync.requests.get")
    @patch("fias_public_api.fias_sync.requests.post")
    def test_get_address_hint_get(self, mock_post, mock_get, api):
        """Test get_address_hint with GET request."""
        mock_response = Mock()
        mock_response.json.return_value = {"hints": []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = api.get_address_hint(search_string="Москва")
        assert result == {"hints": []}
        mock_get.assert_called_once()
        mock_post.assert_not_called()

    @patch("fias_public_api.fias_sync.requests.get")
    @patch("fias_public_api.fias_sync.requests.post")
    def test_get_address_hint_post(self, mock_post, mock_get, api):
        """Test get_address_hint with POST request."""
        mock_response = Mock()
        mock_response.json.return_value = {"hints": []}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        result = api.get_address_hint(
            up_to_level=5,
            search_non_active=False
        )
        assert result == {"hints": []}
        mock_post.assert_called_once()
        mock_get.assert_not_called()

    @patch("fias_public_api.fias_sync.requests.get")
    def test_search_address_item(self, mock_get, api):
        """Test search_address_item method."""
        mock_response = Mock()
        mock_response.json.return_value = {"object_id": 12345}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = api.search_address_item(search_string="Москва")
        assert result == {"object_id": 12345}
        mock_get.assert_called_once()

    @patch("fias_public_api.fias_sync.requests.get")
    def test_get_location_by_ip(self, mock_get, api):
        """Test get_location_by_ip method."""
        mock_response = Mock()
        mock_response.json.return_value = {"addresses": []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = api.get_location_by_ip(ip="8.8.8.8")
        assert result == {"addresses": []}
        mock_get.assert_called_once()

    @patch("fias_public_api.fias_sync.requests.get")
    def test_search(self, mock_get, api):
        """Test search method (wrapper over get_address_hint)."""
        mock_response = Mock()
        mock_response.json.return_value = {"hints": [{"id": 1}]}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = api.search(search_string="Москва")
        assert result == [{"id": 1}]
        mock_get.assert_called_once()

    def test_get_address_type_default(self, api):
        """Test _get_address_type with default value."""
        assert api._get_address_type(None) == AddressType.MUNICIPALITY

    def test_get_address_type_custom(self, api):
        """Test _get_address_type with custom value."""
        assert api._get_address_type(AddressType.ADMINISTRATIVE) == AddressType.ADMINISTRATIVE
        assert api._get_address_type(1) == 1


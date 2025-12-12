"""
Tests for asynchronous FIAS Public API client.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from fias_public_api import AsyncFPA, get_token_async, AddressType


class TestGetTokenAsync:
    """Tests for get_token_async function."""

    @pytest.mark.asyncio
    @patch("fias_public_api.fias_async.httpx.AsyncClient")
    async def test_get_token_success(self, mock_client_class):
        """Test successful token retrieval."""
        mock_client = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"Token": "test-token-123"}
        mock_response.raise_for_status = Mock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client_class.return_value = mock_client

        token = await get_token_async()
        assert token == "test-token-123"

    @pytest.mark.asyncio
    @patch("fias_public_api.fias_async.httpx.AsyncClient")
    async def test_get_token_failure(self, mock_client_class):
        """Test token retrieval failure."""
        mock_client = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 400
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client_class.return_value = mock_client

        with pytest.raises(ValueError, match="Не удалось получить токен"):
            await get_token_async()


class TestAsyncFPA:
    """Tests for AsyncFPA class."""

    @pytest.fixture
    def api(self):
        """Create AsyncFPA instance for testing."""
        return AsyncFPA(token="test-token")

    @pytest.fixture
    def api_with_address_type(self):
        """Create AsyncFPA instance with custom address type."""
        return AsyncFPA(token="test-token", address_type=AddressType.ADMINISTRATIVE)

    @pytest.mark.asyncio
    async def test_get_regions(self, api):
        """Test get_regions method."""
        mock_response = Mock()
        mock_response.json.return_value = {"addresses": []}
        mock_response.raise_for_status = Mock()
        
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        api._client = mock_client

        result = await api.get_regions()
        assert result == {"addresses": []}
        mock_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_address_items(self, api):
        """Test get_address_items method."""
        mock_response = Mock()
        mock_response.json.return_value = {"addresses": []}
        mock_response.raise_for_status = Mock()
        
        mock_client = AsyncMock()
        mock_client.post = AsyncMock(return_value=mock_response)
        api._client = mock_client

        result = await api.get_address_items(
            path="test-path",
            address_level=1
        )
        assert result == {"addresses": []}
        mock_client.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_details(self, api):
        """Test get_details method."""
        mock_response = Mock()
        mock_response.json.return_value = {"address_details": {}}
        mock_response.raise_for_status = Mock()
        
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        api._client = mock_client

        result = await api.get_details(object_id=12345)
        assert result == {"address_details": {}}
        mock_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_details_by_id_with_address_type(self, api_with_address_type):
        """Test details_by_id with custom address type from constructor."""
        mock_response = Mock()
        mock_response.json.return_value = {"addresses": []}
        mock_response.raise_for_status = Mock()
        
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        api_with_address_type._client = mock_client

        result = await api_with_address_type.details_by_id(object_id=12345)
        assert result == {"addresses": []}
        call_args = mock_client.get.call_args
        assert "address_type" in call_args[1]["params"]
        assert call_args[1]["params"]["address_type"] == AddressType.ADMINISTRATIVE

    @pytest.mark.asyncio
    async def test_search(self, api):
        """Test search method."""
        mock_response = Mock()
        mock_response.json.return_value = {"hints": [{"id": 1}]}
        mock_response.raise_for_status = Mock()
        
        mock_client = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        api._client = mock_client

        result = await api.search(search_string="Москва")
        assert result == [{"id": 1}]
        mock_client.get.assert_called_once()

    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager."""
        api = AsyncFPA(token="test-token")
        
        async with api:
            assert api._client is not None
            assert api.client is not None
        
        # After context exit, client should be closed
        assert api._client is None

    def test_get_address_type_default(self, api):
        """Test _get_address_type with default value."""
        assert api._get_address_type(None) == AddressType.MUNICIPALITY

    def test_get_address_type_custom(self, api):
        """Test _get_address_type with custom value."""
        assert api._get_address_type(AddressType.ADMINISTRATIVE) == AddressType.ADMINISTRATIVE


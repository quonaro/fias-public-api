"""
Tests for constants module.
"""

import pytest
from fias_public_api import AddressType, STANDART_HEADERS, retry_on_error
import time


class TestAddressType:
    """Tests for AddressType enum."""

    def test_address_type_values(self):
        """Test AddressType enum values."""
        assert AddressType.ADMINISTRATIVE == 1
        assert AddressType.MUNICIPALITY == 2

    def test_address_type_int_conversion(self):
        """Test AddressType can be used as int."""
        assert int(AddressType.ADMINISTRATIVE) == 1
        assert int(AddressType.MUNICIPALITY) == 2


class TestStandartHeaders:
    """Tests for STANDART_HEADERS function."""

    def test_standart_headers(self):
        """Test STANDART_HEADERS function."""
        token = "test-token-123"
        headers = STANDART_HEADERS(token)
        
        assert headers["accept"] == "application/json"
        assert headers["master-token"] == token
        assert headers["Content-Type"] == "application/json"


class TestRetryOnError:
    """Tests for retry_on_error decorator."""

    def test_retry_on_error_success(self):
        """Test retry decorator with successful call."""
        call_count = 0

        @retry_on_error(max_retries=3, delay=0.1)
        def test_func():
            nonlocal call_count
            call_count += 1
            return "success"

        result = test_func()
        assert result == "success"
        assert call_count == 1

    def test_retry_on_error_retry(self):
        """Test retry decorator with retries."""
        call_count = 0

        @retry_on_error(max_retries=3, delay=0.1)
        def test_func():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("Test error")
            return "success"

        result = test_func()
        assert result == "success"
        assert call_count == 2

    def test_retry_on_error_max_retries(self):
        """Test retry decorator with max retries exceeded."""
        call_count = 0

        @retry_on_error(max_retries=3, delay=0.1)
        def test_func():
            nonlocal call_count
            call_count += 1
            raise ValueError("Test error")

        with pytest.raises(ValueError, match="Test error"):
            test_func()
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_retry_on_error_async(self):
        """Test retry decorator with async function."""
        call_count = 0

        @retry_on_error(max_retries=3, delay=0.1)
        async def test_func():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("Test error")
            return "success"

        result = await test_func()
        assert result == "success"
        assert call_count == 2


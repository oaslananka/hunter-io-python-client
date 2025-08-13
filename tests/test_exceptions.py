"""Tests for Hunter.io API exceptions."""

from hunter_client.exceptions import HunterAPIError, HunterAuthError, HunterRateLimitError


class TestHunterAPIError:
    """Test cases for HunterAPIError."""

    def test_basic_error(self) -> None:
        """Test basic error creation."""
        error = HunterAPIError('Test error')
        
        assert str(error) == 'Test error'
        assert error.message == 'Test error'
        assert error.status_code == 0

    def test_error_with_status_code(self) -> None:
        """Test error with status code."""
        error = HunterAPIError('Test error', 400)
        
        assert str(error) == 'Test error'
        assert error.message == 'Test error'
        assert error.status_code == 400


class TestHunterAuthError:
    """Test cases for HunterAuthError."""

    def test_auth_error(self) -> None:
        """Test authentication error."""
        error = HunterAuthError('Invalid API key', 401)
        
        assert str(error) == 'Invalid API key'
        assert error.message == 'Invalid API key'
        assert error.status_code == 401
        assert isinstance(error, HunterAPIError)


class TestHunterRateLimitError:
    """Test cases for HunterRateLimitError."""

    def test_rate_limit_error(self) -> None:
        """Test rate limit error."""
        error = HunterRateLimitError('Rate limit exceeded', 429)
        
        assert str(error) == 'Rate limit exceeded'
        assert error.message == 'Rate limit exceeded'
        assert error.status_code == 429
        assert isinstance(error, HunterAPIError)

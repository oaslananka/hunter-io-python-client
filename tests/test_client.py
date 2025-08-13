"""Tests for Hunter.io API client."""

from unittest.mock import Mock, patch

import pytest
import requests

from hunter_client import HunterClient
from hunter_client.exceptions import (
    HunterAPIError,
    HunterAuthError,
    HunterRateLimitError,
)


class TestHunterClient:
    """Test cases for HunterClient."""

    def test_init_valid_api_key(self) -> None:
        """Test client initialization with valid API key."""
        client = HunterClient('test-api-key')
        assert client.api_key == 'test-api-key'
        assert client.timeout == 30
        assert isinstance(client.session, requests.Session)

    def test_init_empty_api_key(self) -> None:
        """Test client initialization with empty API key."""
        with pytest.raises(ValueError, match='API key is required'):
            HunterClient('')

    def test_init_custom_timeout(self) -> None:
        """Test client initialization with custom timeout."""
        client = HunterClient('test-api-key', timeout=60)
        assert client.timeout == 60

    @patch('hunter_client.client.requests.Session.request')
    def test_make_request_success(self, mock_request: Mock) -> None:
        """Test successful API request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': {'test': 'value'}}
        mock_request.return_value = mock_response

        client = HunterClient('test-api-key')
        result = client._make_request('test-endpoint')

        assert result == {'data': {'test': 'value'}}
        mock_request.assert_called_once()

    @patch('hunter_client.client.requests.Session.request')
    def test_make_request_auth_error(self, mock_request: Mock) -> None:
        """Test API request with authentication error."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_request.return_value = mock_response

        client = HunterClient('test-api-key')
        
        with pytest.raises(HunterAuthError) as exc_info:
            client._make_request('test-endpoint')
        
        assert exc_info.value.status_code == 401
        assert 'Invalid API key' in str(exc_info.value)

    @patch('hunter_client.client.requests.Session.request')
    def test_make_request_rate_limit_error(self, mock_request: Mock) -> None:
        """Test API request with rate limit error."""
        mock_response = Mock()
        mock_response.status_code = 429
        mock_request.return_value = mock_response

        client = HunterClient('test-api-key')
        
        with pytest.raises(HunterRateLimitError) as exc_info:
            client._make_request('test-endpoint')
        
        assert exc_info.value.status_code == 429
        assert 'Rate limit exceeded' in str(exc_info.value)

    @patch('hunter_client.client.requests.Session.request')
    def test_make_request_generic_error(self, mock_request: Mock) -> None:
        """Test API request with generic error."""
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            'errors': [{'details': 'Invalid domain parameter'}],
        }
        mock_request.return_value = mock_response

        client = HunterClient('test-api-key')
        
        with pytest.raises(HunterAPIError) as exc_info:
            client._make_request('test-endpoint')
        
        assert exc_info.value.status_code == 400
        assert 'Invalid domain parameter' in str(exc_info.value)

    @patch('hunter_client.client.requests.Session.request')
    def test_make_request_connection_error(self, mock_request: Mock) -> None:
        """Test API request with connection error."""
        mock_request.side_effect = requests.exceptions.ConnectionError('Network error')

        client = HunterClient('test-api-key')
        
        with pytest.raises(HunterAPIError) as exc_info:
            client._make_request('test-endpoint')
        
        assert 'Request failed' in str(exc_info.value)

    def test_domain_search_no_params(self) -> None:
        """Test domain search without domain or company."""
        client = HunterClient('test-api-key')
        
        with pytest.raises(ValueError, match='Either domain or company must be provided'):
            client.domain_search()

    @patch('hunter_client.client.HunterClient._make_request')
    def test_domain_search_with_domain(self, mock_request: Mock) -> None:
        """Test domain search with domain parameter."""
        mock_request.return_value = {
            'data': {
                'domain': 'example.com',
                'disposable': False,
                'webmail': False,
                'accept_all': True,
                'emails': [],
                'linked_domains': [],
            },
            'meta': {
                'results': 0,
                'limit': 10,
                'offset': 0,
                'params': {'domain': 'example.com'},
            },
        }

        client = HunterClient('test-api-key')
        response = client.domain_search(domain='example.com')

        assert response.data.domain == 'example.com'
        assert not response.data.disposable
        mock_request.assert_called_once_with('domain-search', {'domain': 'example.com'})

    def test_email_finder_no_domain_or_company(self) -> None:
        """Test email finder without domain or company."""
        client = HunterClient('test-api-key')
        
        with pytest.raises(ValueError, match='Either domain or company must be provided'):
            client.email_finder()

    def test_email_finder_no_name(self) -> None:
        """Test email finder without name parameters."""
        client = HunterClient('test-api-key')
        
        with pytest.raises(ValueError, match='Either first_name and last_name, or full_name must be provided'):
            client.email_finder(domain='example.com')

    @patch('hunter_client.client.HunterClient._make_request')
    def test_email_finder_success(self, mock_request: Mock) -> None:
        """Test successful email finder request."""
        mock_request.return_value = {
            'data': {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@example.com',
                'score': 95,
                'domain': 'example.com',
                'accept_all': False,
                'sources': [],
            },
            'meta': {
                'params': {
                    'domain': 'example.com',
                    'first_name': 'John',
                    'last_name': 'Doe',
                },
            },
        }

        client = HunterClient('test-api-key')
        response = client.email_finder(
            domain='example.com',
            first_name='John',
            last_name='Doe',
        )

        assert response.data.email == 'john.doe@example.com'
        assert response.data.score == 95
        mock_request.assert_called_once()

    def test_email_verifier_empty_email(self) -> None:
        """Test email verifier with empty email."""
        client = HunterClient('test-api-key')
        
        with pytest.raises(ValueError, match='Email address is required'):
            client.email_verifier('')

    @patch('hunter_client.client.HunterClient._make_request')
    def test_email_verifier_success(self, mock_request: Mock) -> None:
        """Test successful email verification request."""
        mock_request.return_value = {
            'data': {
                'status': 'valid',
                'result': 'deliverable',
                'score': 100,
                'email': 'test@example.com',
                'regexp': True,
                'gibberish': False,
                'disposable': False,
                'webmail': False,
                'mx_records': True,
                'smtp_server': True,
                'smtp_check': True,
                'accept_all': False,
                'block': False,
                'sources': [],
            },
            'meta': {
                'params': {'email': 'test@example.com'},
            },
        }

        client = HunterClient('test-api-key')
        response = client.email_verifier('test@example.com')

        assert response.data.status == 'valid'
        assert response.data.score == 100
        mock_request.assert_called_once_with('email-verifier', {'email': 'test@example.com'})

# Hunter.io Python Client

A Python client library for the Hunter.io API, providing easy access to email discovery and verification services.

## Features

- **Domain Search**: Find email addresses associated with a domain
- **Email Finder**: Find specific email addresses using names and domain
- **Email Verifier**: Verify the deliverability of email addresses
- **Type Safety**: Full type hints and Pydantic models
- **Error Handling**: Comprehensive exception handling
- **Rate Limiting**: Built-in handling of API rate limits

## Installation

```bash
pip install hunter-io-client
```

## Quick Start

```python
from hunter_client import HunterClient

# Initialize the client
client = HunterClient('your-api-key')

# Search for emails in a domain
domain_result = client.domain_search(domain='example.com')
print(f"Found {len(domain_result.data.emails)} emails")

# Find a specific person's email
email_result = client.email_finder(
    domain='example.com',
    first_name='John',
    last_name='Doe'
)
print(f"Email: {email_result.data.email}")

# Verify an email address
verification = client.email_verifier('test@example.com')
print(f"Status: {verification.data.status}")
```

## API Reference

### HunterClient

#### Constructor

```python
client = HunterClient(api_key, timeout=30)
```

- `api_key` (str): Your Hunter.io API key
- `timeout` (int): Request timeout in seconds (default: 30)

#### Methods

##### domain_search()

Search for email addresses associated with a domain.

```python
response = client.domain_search(
    domain='example.com',
    company='Example Corp',  # Alternative to domain
    limit=10,
    offset=0,
    type_filter='personal',  # 'personal' or 'generic'
    seniority='executive',
    department='sales',
    required_field='full_name'
)
```

##### email_finder()

Find the most likely email address for a person.

```python
response = client.email_finder(
    domain='example.com',
    company='Example Corp',  # Alternative to domain
    first_name='John',
    last_name='Doe',
    full_name='John Doe',  # Alternative to first/last name
    max_duration=10
)
```

##### email_verifier()

Verify the deliverability of an email address.

```python
response = client.email_verifier('test@example.com')
```

## Error Handling

The client raises specific exceptions for different error conditions:

```python
from hunter_client import HunterClient
from hunter_client.exceptions import (
    HunterAPIError,
    HunterAuthError,
    HunterRateLimitError
)

client = HunterClient('your-api-key')

try:
    result = client.domain_search(domain='example.com')
except HunterAuthError:
    print("Invalid API key")
except HunterRateLimitError:
    print("Rate limit exceeded")
except HunterAPIError as e:
    print(f"API error: {e.message} (status: {e.status_code})")
```

## Response Models

All API responses are returned as typed Pydantic models:

- `DomainSearchResponse`: Contains domain information and found emails
- `EmailFinderResponse`: Contains the found email and associated data
- `EmailVerificationResponse`: Contains verification results and scores

## Requirements

- Python 3.11+
- requests >= 2.31.0
- pydantic >= 2.5.0

## Development

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running Tests

```bash
pytest
```

### Code Quality

```bash
# Run linting
flake8 .

# Run type checking
mypy .

# Format code
black .
isort .
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## API Documentation

For detailed API documentation, visit: [Hunter.io API Documentation](https://hunter.io/api-documentation/v2)

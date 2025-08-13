"""Hunter.io API Client.

A Python client library for the Hunter.io API.
Provides access to domain search, email finder, and email verification endpoints.
"""

from .client import HunterClient
from .exceptions import HunterAPIError, HunterAuthError, HunterRateLimitError
from .models import DomainSearchResponse, EmailFinderResponse, EmailVerificationResponse

__version__ = "1.0.0"
__all__ = [
    "HunterClient",
    "HunterAPIError",
    "HunterAuthError",
    "HunterRateLimitError",
    "DomainSearchResponse",
    "EmailFinderResponse",
    "EmailVerificationResponse",
]

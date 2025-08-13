"""Hunter.io API exceptions."""


class HunterAPIError(Exception):
    """Base exception for Hunter.io API errors."""

    def __init__(self, message: str, status_code: int = 0) -> None:
        """Initialize Hunter API error.

        Args:
            message: Error message
            status_code: HTTP status code
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class HunterAuthError(HunterAPIError):
    """Authentication error for Hunter.io API."""


class HunterRateLimitError(HunterAPIError):
    """Rate limit exceeded error for Hunter.io API."""

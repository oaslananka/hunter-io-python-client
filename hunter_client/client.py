"""Hunter.io API Client."""

from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests

from .exceptions import HunterAPIError, HunterAuthError, HunterRateLimitError
from .models import DomainSearchResponse, EmailFinderResponse, EmailVerificationResponse


class HunterClient:
    """Hunter.io API client."""

    def __init__(self, api_key: str, timeout: int = 30) -> None:
        """Initialize Hunter client.

        Args:
            api_key: Hunter.io API key
            timeout: Request timeout in seconds

        Raises:
            ValueError: If api_key is empty
        """
        if not api_key:
            raise ValueError("API key is required")

        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.base_url = "https://api.hunter.io/v2/"

    def _make_request(
        self,
        endpoint: str,
        request_params: Optional[Dict[str, Any]] = None,
        method: str = "GET",
    ) -> Dict[str, Any]:
        """Make HTTP request to Hunter API.

        Args:
            endpoint: API endpoint
            request_params: Request parameters
            method: HTTP method

        Returns:
            JSON response data

        Raises:
            HunterAuthError: Authentication error
            HunterRateLimitError: Rate limit exceeded
            HunterAPIError: Other API errors
        """
        url = urljoin(self.base_url, endpoint)

        if request_params is None:
            request_params = {}

        request_params["api_key"] = self.api_key

        return self._execute_request(method, url, request_params)

    def _execute_request(
        self,
        method: str,
        url: str,
        request_params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Execute the HTTP request and handle response.

        Args:
            method: HTTP method
            url: Request URL
            request_params: Request parameters

        Returns:
            JSON response data

        Raises:
            HunterAuthError: Authentication error
            HunterRateLimitError: Rate limit exceeded
            HunterAPIError: Other API errors
        """
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=request_params,
                timeout=self.timeout,
            )
        except requests.exceptions.RequestException as request_exc:
            raise HunterAPIError(f"Request failed: {request_exc}") from request_exc

        return self._process_response(response)

    def _process_response(self, response: requests.Response) -> Dict[str, Any]:
        """Process HTTP response and handle errors.

        Args:
            response: HTTP response object

        Returns:
            JSON response data

        Raises:
            HunterAuthError: Authentication error
            HunterRateLimitError: Rate limit exceeded
            HunterAPIError: Other API errors
        """
        unauthorized_status_code = 401
        rate_limit_status_code = 429
        bad_request_status_code = 400

        if response.status_code == unauthorized_status_code:
            raise HunterAuthError("Invalid API key", response.status_code)
        elif response.status_code == rate_limit_status_code:
            raise HunterRateLimitError("Rate limit exceeded", response.status_code)
        elif response.status_code >= bad_request_status_code:
            error_message = self._extract_error_message(response)
            raise HunterAPIError(error_message, response.status_code)

        return self._parse_json_response(response)

    def _extract_error_message(self, response: requests.Response) -> str:
        """Extract error message from response.

        Args:
            response: HTTP response object

        Returns:
            Error message string
        """
        error_message = "API request failed"
        try:
            error_data = response.json()
            if "errors" in error_data:
                errors = error_data["errors"]
                if errors and isinstance(errors, list):
                    error_message = errors[0].get("details", error_message)
        except (ValueError, KeyError):
            # Use default error message if JSON parsing fails
            pass
        return error_message

    def _parse_json_response(self, response: requests.Response) -> Dict[str, Any]:
        """Parse JSON response.

        Args:
            response: HTTP response object

        Returns:
            Parsed JSON data

        Raises:
            HunterAPIError: If JSON parsing fails
        """
        try:
            return response.json()
        except ValueError as json_exc:
            raise HunterAPIError(f"Invalid JSON response: {json_exc}") from json_exc

    def domain_search(
        self,
        domain: Optional[str] = None,
        company: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        type_filter: Optional[str] = None,
        seniority: Optional[str] = None,
        department: Optional[str] = None,
        required_field: Optional[str] = None,
    ) -> DomainSearchResponse:
        """Search for email addresses for a given domain or company.

        Args:
            domain: Domain name to search
            company: Company name to search
            limit: Maximum number of results
            offset: Number of results to skip
            type_filter: Filter by email type (personal/generic)
            seniority: Filter by seniority level
            department: Filter by department
            required_field: Required fields filter

        Returns:
            Domain search response

        Raises:
            ValueError: If neither domain nor company is provided
        """
        if not domain and not company:
            raise ValueError("Either domain or company must be provided")

        request_params: Dict[str, Any] = {}

        if domain:
            request_params["domain"] = domain
        if company:
            request_params["company"] = company
        if limit is not None:
            request_params["limit"] = limit
        if offset is not None:
            request_params["offset"] = offset
        if type_filter:
            request_params["type"] = type_filter
        if seniority:
            request_params["seniority"] = seniority
        if department:
            request_params["department"] = department
        if required_field:
            request_params["required_field"] = required_field

        response_data = self._make_request("domain-search", request_params)
        return DomainSearchResponse(**response_data)

    def email_finder(
        self,
        domain: Optional[str] = None,
        company: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        full_name: Optional[str] = None,
        max_duration: Optional[int] = None,
    ) -> EmailFinderResponse:
        """Find email address for a person.

        Args:
            domain: Domain name
            company: Company name
            first_name: Person's first name
            last_name: Person's last name
            full_name: Person's full name
            max_duration: Maximum request duration

        Returns:
            Email finder response

        Raises:
            ValueError: If required parameters are missing
        """
        self._validate_email_finder_params(
            domain,
            company,
            first_name,
            last_name,
            full_name,
        )

        request_params: Dict[str, Any] = {}

        if domain:
            request_params["domain"] = domain
        if company:
            request_params["company"] = company
        if first_name:
            request_params["first_name"] = first_name
        if last_name:
            request_params["last_name"] = last_name
        if full_name:
            request_params["full_name"] = full_name
        if max_duration is not None:
            request_params["max_duration"] = max_duration

        response_data = self._make_request("email-finder", request_params)
        return EmailFinderResponse(**response_data)

    def _validate_email_finder_params(
        self,
        domain: Optional[str],
        company: Optional[str],
        first_name: Optional[str],
        last_name: Optional[str],
        full_name: Optional[str],
    ) -> None:
        """Validate email finder parameters.

        Args:
            domain: Domain name
            company: Company name
            first_name: Person's first name
            last_name: Person's last name
            full_name: Person's full name

        Raises:
            ValueError: If required parameters are missing
        """
        if not domain and not company:
            raise ValueError("Either domain or company must be provided")

        has_first_and_last = first_name and last_name
        if not has_first_and_last and not full_name:
            error_msg = "Either first_name and last_name, or full_name must be provided"
            raise ValueError(error_msg)

    def email_verifier(self, email: str) -> EmailVerificationResponse:
        """Verify an email address.

        Args:
            email: Email address to verify

        Returns:
            Email verification response

        Raises:
            ValueError: If email is empty
        """
        if not email:
            raise ValueError("Email address is required")

        request_params = {"email": email}
        response_data = self._make_request("email-verifier", request_params)
        return EmailVerificationResponse(**response_data)

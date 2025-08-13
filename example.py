"""Example usage of Hunter.io Python client."""

from hunter_client import HunterClient
from hunter_client.exceptions import HunterAPIError, HunterAuthError, HunterRateLimitError


def main() -> None:
    """Demonstrate Hunter.io API client usage."""
    # Initialize the client with your API key
    # You can get a free API key at: https://hunter.io/users/sign_up
    api_key = "your-api-key-here"  # Replace with your actual API key
    
    if api_key == "your-api-key-here":
        print("Please replace 'your-api-key-here' with your actual Hunter.io API key")
        return
    
    client = HunterClient(api_key)
    
    # Example 1: Domain Search
    print("=== Domain Search Example ===")
    try:
        domain_result = client.domain_search(domain="stripe.com", limit=5)
        print(f"Found {len(domain_result.data.emails)} emails for {domain_result.data.domain}")
        
        for email in domain_result.data.emails:
            print(f"  - {email.value} ({email.type}, confidence: {email.confidence}%)")
            
    except HunterAPIError as e:
        print(f"Domain search error: {e.message} (status: {e.status_code})")
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Email Finder
    print("=== Email Finder Example ===")
    try:
        finder_result = client.email_finder(
            domain="stripe.com",
            first_name="Patrick",
            last_name="Collison"
        )
        
        print(f"Found email: {finder_result.data.email}")
        print(f"Confidence score: {finder_result.data.score}%")
        print(f"Position: {finder_result.data.position}")
        
    except HunterAPIError as e:
        print(f"Email finder error: {e.message} (status: {e.status_code})")
    
    print("\n" + "="*50 + "\n")
    
    # Example 3: Email Verification
    print("=== Email Verification Example ===")
    try:
        verification_result = client.email_verifier("test@example.com")
        
        print(f"Email: {verification_result.data.email}")
        print(f"Status: {verification_result.data.status}")
        print(f"Score: {verification_result.data.score}%")
        print(f"Deliverable: {verification_result.data.result}")
        print(f"Valid format: {verification_result.data.regexp}")
        print(f"MX records exist: {verification_result.data.mx_records}")
        
    except HunterAPIError as e:
        print(f"Email verification error: {e.message} (status: {e.status_code})")
    
    print("\n" + "="*50 + "\n")
    
    # Example 4: Error Handling
    print("=== Error Handling Example ===")
    try:
        # This will fail because we're not providing domain or company
        client.domain_search()
        
    except ValueError as e:
        print(f"Validation error: {e}")
    except HunterAuthError:
        print("Authentication failed - check your API key")
    except HunterRateLimitError:
        print("Rate limit exceeded - please wait before making more requests")
    except HunterAPIError as e:
        print(f"API error: {e.message} (status: {e.status_code})")


if __name__ == "__main__":
    main()

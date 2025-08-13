"""Tests for Hunter.io API models."""

from hunter_client.models import (
    DomainSearchData,
    DomainSearchResponse,
    Email,
    EmailFinderData,
    EmailFinderResponse,
    EmailSource,
    EmailVerification,
    EmailVerificationData,
    EmailVerificationResponse,
    Meta,
)


class TestEmailSource:
    """Test cases for EmailSource model."""

    def test_valid_email_source(self) -> None:
        """Test valid email source creation."""
        source = EmailSource(
            domain='example.com',
            uri='https://example.com/contact',
            extracted_on='2023-01-01',
            last_seen_on='2023-01-02',
            still_on_page=True,
        )
        
        assert source.domain == 'example.com'
        assert source.uri == 'https://example.com/contact'
        assert source.still_on_page is True


class TestEmailVerification:
    """Test cases for EmailVerification model."""

    def test_valid_verification(self) -> None:
        """Test valid email verification creation."""
        verification = EmailVerification(
            date='2023-01-01',
            status='valid',
        )
        
        assert verification.date == '2023-01-01'
        assert verification.status == 'valid'

    def test_optional_fields(self) -> None:
        """Test optional fields in email verification."""
        verification = EmailVerification()
        
        assert verification.date is None
        assert verification.status is None


class TestEmail:
    """Test cases for Email model."""

    def test_valid_email(self) -> None:
        """Test valid email creation."""
        email = Email(
            value='test@example.com',
            type='personal',
            confidence=95,
        )

        assert email.value == 'test@example.com'
        assert email.type == 'personal'
        assert email.confidence == 95
        assert email.sources == []

    def test_email_with_sources(self) -> None:
        """Test email with sources."""
        source = EmailSource(
            domain='example.com',
            uri='https://example.com',
            extracted_on='2023-01-01',
            last_seen_on='2023-01-02',
            still_on_page=True,
        )
        
        email = Email(
            value='test@example.com',
            type='personal',
            confidence=95,
            sources=[source],
        )
        
        assert len(email.sources) == 1
        assert email.sources[0].domain == 'example.com'


class TestDomainSearchData:
    """Test cases for DomainSearchData model."""

    def test_minimal_domain_search_data(self) -> None:
        """Test minimal domain search data creation."""
        data = DomainSearchData(
            domain='example.com',
            disposable=False,
            webmail=False,
            accept_all=True,
        )
        
        assert data.domain == 'example.com'
        assert data.disposable is False
        assert data.webmail is False
        assert data.accept_all is True
        assert data.emails == []
        assert data.technologies == []

    def test_full_domain_search_data(self) -> None:
        """Test full domain search data creation."""
        email = Email(
            value='test@example.com',
            type='personal',
            confidence=95,
        )
        
        data = DomainSearchData(
            domain='example.com',
            disposable=False,
            webmail=False,
            accept_all=True,
            organization='Example Corp',
            industry='Technology',
            country='US',
            emails=[email],
            technologies=['python', 'django'],
        )
        
        assert data.organization == 'Example Corp'
        assert data.industry == 'Technology'
        assert data.country == 'US'
        assert len(data.emails) == 1
        assert len(data.technologies) == 2


class TestDomainSearchResponse:
    """Test cases for DomainSearchResponse model."""

    def test_valid_domain_search_response(self) -> None:
        """Test valid domain search response creation."""
        data = DomainSearchData(
            domain='example.com',
            disposable=False,
            webmail=False,
            accept_all=True,
        )
        
        meta = Meta(
            results=1,
            limit=10,
            offset=0,
        )
        
        response = DomainSearchResponse(data=data, meta=meta)
        
        assert response.data.domain == 'example.com'
        assert response.meta.results == 1


class TestEmailFinderData:
    """Test cases for EmailFinderData model."""

    def test_valid_email_finder_data(self) -> None:
        """Test valid email finder data creation."""
        data = EmailFinderData(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            score=95,
            domain='example.com',
            accept_all=False,
        )
        
        assert data.first_name == 'John'
        assert data.last_name == 'Doe'
        assert data.email == 'john.doe@example.com'
        assert data.score == 95
        assert data.domain == 'example.com'
        assert data.accept_all is False


class TestEmailFinderResponse:
    """Test cases for EmailFinderResponse model."""

    def test_valid_email_finder_response(self) -> None:
        """Test valid email finder response creation."""
        data = EmailFinderData(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            score=95,
            domain='example.com',
            accept_all=False,
        )
        
        meta = Meta()
        
        response = EmailFinderResponse(data=data, meta=meta)
        
        assert response.data.email == 'john.doe@example.com'


class TestEmailVerificationData:
    """Test cases for EmailVerificationData model."""

    def test_valid_verification_data(self) -> None:
        """Test valid email verification data creation."""
        data = EmailVerificationData(
            status='valid',
            result='deliverable',
            score=100,
            email='test@example.com',
            regexp=True,
            gibberish=False,
            disposable=False,
            webmail=False,
            mx_records=True,
            smtp_server=True,
            smtp_check=True,
            accept_all=False,
            block=False,
        )
        
        assert data.status == 'valid'
        assert data.result == 'deliverable'
        assert data.score == 100
        assert data.email == 'test@example.com'
        assert data.regexp is True
        assert data.sources == []


class TestEmailVerificationResponse:
    """Test cases for EmailVerificationResponse model."""

    def test_valid_verification_response(self) -> None:
        """Test valid email verification response creation."""
        data = EmailVerificationData(
            status='valid',
            result='deliverable',
            score=100,
            email='test@example.com',
            regexp=True,
            gibberish=False,
            disposable=False,
            webmail=False,
            mx_records=True,
            smtp_server=True,
            smtp_check=True,
            accept_all=False,
            block=False,
        )
        
        meta = Meta()
        
        response = EmailVerificationResponse(data=data, meta=meta)
        
        assert response.data.status == 'valid'
        assert response.data.email == 'test@example.com'

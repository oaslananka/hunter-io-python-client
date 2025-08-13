"""Hunter.io API response models."""

from typing import List, Optional

from pydantic import BaseModel, Field


class EmailSource(BaseModel):
    """Email source information."""

    domain: str
    uri: str
    extracted_on: str
    last_seen_on: str
    still_on_page: bool


class EmailVerification(BaseModel):
    """Email verification information."""

    date: Optional[str] = None
    status: Optional[str] = None


class Email(BaseModel):
    """Email address information."""

    value: str  # noqa: WPS110
    type: str  # noqa: WPS110
    confidence: int
    sources: List[EmailSource] = Field(default_factory=list)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    position: Optional[str] = None
    seniority: Optional[str] = None
    department: Optional[str] = None
    linkedin: Optional[str] = None
    twitter: Optional[str] = None
    phone_number: Optional[str] = None
    verification: Optional[EmailVerification] = None


class DomainSearchData(BaseModel):
    """Domain search response data."""

    domain: str
    disposable: bool
    webmail: bool
    accept_all: bool
    pattern: Optional[str] = None
    organization: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    twitter: Optional[str] = None
    facebook: Optional[str] = None
    linkedin: Optional[str] = None
    instagram: Optional[str] = None
    youtube: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    street: Optional[str] = None
    headcount: Optional[str] = None
    company_type: Optional[str] = None
    emails: List[Email] = Field(default_factory=list)
    linked_domains: List[str] = Field(default_factory=list)


class MetaParams(BaseModel):
    """Meta parameters information."""

    domain: Optional[str] = None
    company: Optional[str] = None
    type: Optional[str] = None
    seniority: Optional[str] = None
    department: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None


class Meta(BaseModel):
    """Meta information for API responses."""

    results: Optional[int] = None  # noqa: WPS110
    limit: Optional[int] = None
    offset: Optional[int] = None
    params: Optional[MetaParams] = None  # noqa: WPS110


class DomainSearchResponse(BaseModel):
    """Domain search API response."""

    data: DomainSearchData  # noqa: WPS110
    meta: Meta


class EmailFinderData(BaseModel):
    """Email finder response data."""

    first_name: str
    last_name: str
    email: str
    score: int
    domain: str
    accept_all: bool
    position: Optional[str] = None
    twitter: Optional[str] = None
    linkedin_url: Optional[str] = None
    phone_number: Optional[str] = None
    company: Optional[str] = None
    sources: List[EmailSource] = Field(default_factory=list)
    verification: Optional[EmailVerification] = None


class EmailFinderResponse(BaseModel):
    """Email finder API response."""

    data: EmailFinderData  # noqa: WPS110
    meta: Meta


class EmailVerificationData(BaseModel):
    """Email verification response data."""

    status: str
    result: str  # noqa: WPS110
    score: int
    email: str
    regexp: bool
    gibberish: bool
    disposable: bool
    webmail: bool
    mx_records: bool
    smtp_server: bool
    smtp_check: bool
    accept_all: bool
    block: bool
    sources: List[EmailSource] = Field(default_factory=list)


class EmailVerificationResponse(BaseModel):
    """Email verification API response."""

    data: EmailVerificationData  # noqa: WPS110
    meta: Meta

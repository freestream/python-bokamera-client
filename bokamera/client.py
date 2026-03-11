"""
High-level BokaMera API client.

This module exposes :class:`BokaMeraClient`, the main entry point for
interacting with the BokaMera booking API.  All API operations are grouped into
resource namespaces (e.g. ``client.bookings``, ``client.services``) which can
be accessed as properties on the client instance.
"""

from __future__ import annotations

from uuid import UUID

from ._client import BokaMeraHTTPClient
from .resources.articles import ArticleResource
from .resources.billing import BillingResource
from .resources.bookings import BookingResource
from .resources.codelock import CodeLockResource
from .resources.companies import CompanyResource
from .resources.custom_fields import CustomFieldResource
from .resources.customers import CustomerResource
from .resources.eaccounting import EAccountingResource
from .resources.gdpr import GDPRResource
from .resources.homepage import HomepageResource
from .resources.licenses import LicenseResource
from .resources.rebate_codes import RebateCodeResource
from .resources.resources import ResourceResource
from .resources.schedules import ScheduleResource
from .resources.services import ServiceResource
from .resources.support import SupportResource
from .resources.system import SystemResource
from .resources.users import UserResource
from .resources.webhooks import WebhookResource


class BokaMeraClient:
    """
    Synchronous BokaMera API client.

    Usage::

        client = BokaMeraClient(api_key="your-key", company_id="uuid-here")

        # List upcoming bookings
        result = client.bookings.list(booking_start=datetime.now())

        # Get available times for a service
        times = client.services.get_available_times(
            service_id=42,
            from_=datetime(2026, 3, 10),
            to=datetime(2026, 3, 17),
        )

        # Create a booking
        booking = client.bookings.create(
            from_=datetime(2026, 3, 11, 10, 0),
            to=datetime(2026, 3, 11, 11, 0),
            service_id=42,
            customer={"Firstname": "Anna", "Lastname": "Svensson", "Email": "anna@example.com"},
        )
    """

    def __init__(
        self,
        api_key: str,
        company_id: UUID | str | None = None,
        base_url: str = "https://api.bokamera.se",
        timeout: float = 30.0,
    ) -> None:
        """Create a new BokaMera API client.

        Args:
            api_key: BokaMera API key used for all requests.
            company_id: Optional default company UUID.  When provided it is
                automatically included in every API call that accepts a
                ``CompanyId`` parameter so it does not need to be supplied
                on each individual call.
            base_url: Override for the API base URL (defaults to the
                production endpoint).
            timeout: Per-request HTTP timeout in seconds.
        """
        self._http = BokaMeraHTTPClient(
            api_key=api_key,
            company_id=UUID(str(company_id)) if company_id else None,
            base_url=base_url,
            timeout=timeout,
        )
        self._init_resources()

    def _init_resources(self) -> None:
        """Instantiate all resource namespaces and attach them to the client."""
        self._articles = ArticleResource(self._http)
        self._billing = BillingResource(self._http)
        self._bookings = BookingResource(self._http)
        self._codelock = CodeLockResource(self._http)
        self._companies = CompanyResource(self._http)
        self._custom_fields = CustomFieldResource(self._http)
        self._customers = CustomerResource(self._http)
        self._eaccounting = EAccountingResource(self._http)
        self._gdpr = GDPRResource(self._http)
        self._homepage = HomepageResource(self._http)
        self._licenses = LicenseResource(self._http)
        self._rebate_codes = RebateCodeResource(self._http)
        self._resources = ResourceResource(self._http)
        self._schedules = ScheduleResource(self._http)
        self._services = ServiceResource(self._http)
        self._support = SupportResource(self._http)
        self._system = SystemResource(self._http)
        self._users = UserResource(self._http)
        self._webhooks = WebhookResource(self._http)

    # ── Resource namespaces ──────────────────────────────────────────────────

    @property
    def articles(self) -> ArticleResource:
        """Articles and article types."""
        return self._articles

    @property
    def billing(self) -> BillingResource:
        """Billing information, invoices, payment settings, Stripe and Qvickly."""
        return self._billing

    @property
    def bookings(self) -> BookingResource:
        """Bookings, booking log, booking queue, and reports."""
        return self._bookings

    @property
    def codelock(self) -> CodeLockResource:
        """Code lock integrations (Accessy, Axema, Parakey, Siedle, Zesec, etc.)."""
        return self._codelock

    @property
    def companies(self) -> CompanyResource:
        """Companies, company types, coordinates, owners, and administrators."""
        return self._companies

    @property
    def custom_fields(self) -> CustomFieldResource:
        """Custom fields, slots, and validation rules."""
        return self._custom_fields

    @property
    def customers(self) -> CustomerResource:
        """Customers, customer comments, and customer articles."""
        return self._customers

    @property
    def eaccounting(self) -> EAccountingResource:
        """Visma eEkonomi integration: invoices, drafts, articles, notes."""
        return self._eaccounting

    @property
    def gdpr(self) -> GDPRResource:
        """GDPR customer data export and inactive customer management."""
        return self._gdpr

    @property
    def homepage(self) -> HomepageResource:
        """Homepage settings, images, widget settings, news, and message templates."""
        return self._homepage

    @property
    def licenses(self) -> LicenseResource:
        """Company licenses, license types, plans, and trials."""
        return self._licenses

    @property
    def rebate_codes(self) -> RebateCodeResource:
        """Rebate codes, statuses, types, transactions, and price calculations."""
        return self._rebate_codes

    @property
    def resources(self) -> ResourceResource:
        """Resources, resource types, and time exceptions."""
        return self._resources

    @property
    def schedules(self) -> ScheduleResource:
        """Date schedules and recurring schedules."""
        return self._schedules

    @property
    def services(self) -> ServiceResource:
        """Services, prices, available times, and duration types."""
        return self._services

    @property
    def support(self) -> SupportResource:
        """Support cases, comments, attachments, and statuses."""
        return self._support

    @property
    def system(self) -> SystemResource:
        """System version, settings, categories, ratings, references, countries,
        currencies, Google Meet, and Mailchimp."""
        return self._system

    @property
    def users(self) -> UserResource:
        """User profile, agreements, favorites, and password reset."""
        return self._users

    @property
    def webhooks(self) -> WebhookResource:
        """Webhook endpoints."""
        return self._webhooks

    # ── Context manager ──────────────────────────────────────────────────────

    def close(self) -> None:
        """Close the underlying HTTP client and release resources."""
        self._http.close()

    def __enter__(self) -> BokaMeraClient:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

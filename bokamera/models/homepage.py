"""
Data models for the homepage resource.

Contains dataclasses for homepage settings, navigation menus, images,
booking widget settings, and news items.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from .common import _uuid


@dataclass(slots=True)
class HomepageSettingsResponse:
    """General homepage configuration for a company's BokaMera site.

    Attributes:
        id: Settings record ID.
        company_id: UUID of the owning company.
        enable_homepage: Whether the public homepage is enabled.
        show_rating: Whether the customer rating is displayed on the homepage.
        hero_section_style_id: Style variant for the hero / banner section.
        template_id: Visual template applied to the homepage.
        heading: Main heading text on the homepage.
        body: Body text or HTML content displayed on the homepage.
    """

    id: int | None = None
    company_id: UUID | None = None
    enable_homepage: bool = False
    show_rating: bool = True
    hero_section_style_id: int | None = None
    template_id: int | None = None
    heading: str | None = None
    body: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> HomepageSettingsResponse:
        """Construct a HomepageSettingsResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            company_id=_uuid(d.get("CompanyId")),
            enable_homepage=d.get("EnableHomepage", False),
            show_rating=d.get("ShowRating", True),
            hero_section_style_id=d.get("HeroSectionStyleId"),
            template_id=d.get("TemplateId"),
            heading=d.get("Heading"),
            body=d.get("Body"),
        )


@dataclass(slots=True)
class HomepageMenuResponse:
    """Navigation menu visibility settings for a company's homepage.

    Each attribute controls whether the corresponding menu item is shown.

    Attributes:
        home: Show the Home link.
        services: Show the Services link.
        book_time: Show the Book Now link.
        about_us: Show the About Us link.
        contact_us: Show the Contact Us link.
        my_bookings: Show the My Bookings link.
        calendar: Show the Calendar link.
    """

    home: bool = True
    services: bool = True
    book_time: bool = True
    about_us: bool = True
    contact_us: bool = True
    my_bookings: bool = True
    calendar: bool = False

    @classmethod
    def from_dict(cls, d: dict) -> HomepageMenuResponse:
        """Construct a HomepageMenuResponse from a raw API response dict."""
        return cls(
            home=d.get("Home", True),
            services=d.get("Services", True),
            book_time=d.get("BookTime", True),
            about_us=d.get("AboutUs", True),
            contact_us=d.get("ContactUs", True),
            my_bookings=d.get("MyBookings", True),
            calendar=d.get("Calendar", False),
        )


@dataclass(slots=True)
class HomepageImageResponse:
    """An image displayed in the homepage gallery.

    Attributes:
        id: Image record ID.
        title: Optional title caption for the image.
        description: Optional descriptive text shown alongside the image.
        image_url: Public URL of the image.
    """

    id: int | None = None
    title: str | None = None
    description: str | None = None
    image_url: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> HomepageImageResponse:
        """Construct a HomepageImageResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            title=d.get("Title"),
            description=d.get("Description"),
            image_url=d.get("ImageUrl"),
        )


@dataclass(slots=True)
class HomepageWidgetSettingsResponse:
    """Visual and functional settings for the embeddable booking widget.

    Attributes:
        company_id: UUID of the owning company.
        service_layout_id: Layout variant used for displaying services.
        time_layout_id: Layout variant used for displaying available times.
        booking_layout_id: Layout variant used for the booking confirmation step.
        primary_color: Hex colour code used as the widget's accent colour.
        dark_theme: Whether the dark colour scheme is enabled.
        show_service_image: Whether service images are shown in the widget.
        enable_login: Whether customers must log in before booking.
        enable_direct_booking: Whether customers can skip service selection and
            book directly.
    """

    company_id: UUID | None = None
    service_layout_id: int | None = None
    time_layout_id: int | None = None
    booking_layout_id: int | None = None
    primary_color: str | None = None
    dark_theme: bool = False
    show_service_image: bool = True
    enable_login: bool = True
    enable_direct_booking: bool = False

    @classmethod
    def from_dict(cls, d: dict) -> HomepageWidgetSettingsResponse:
        """Construct a HomepageWidgetSettingsResponse from a raw API response dict."""
        return cls(
            company_id=_uuid(d.get("CompanyId")),
            service_layout_id=d.get("ServiceLayoutId"),
            time_layout_id=d.get("TimeLayoutId"),
            booking_layout_id=d.get("BookingLayoutId"),
            primary_color=d.get("PrimaryColor"),
            dark_theme=d.get("DarkTheme", False),
            show_service_image=d.get("ShowServiceImage", True),
            enable_login=d.get("EnableLogin", True),
            enable_direct_booking=d.get("EnableDirectBooking", False),
        )


@dataclass(slots=True)
class NewsItemResponse:
    """A news or announcement item published on a company's homepage.

    Attributes:
        id: News item ID.
        heading: Headline / title of the news item.
        body: Full body text (may contain HTML).
        image_url: Optional URL of an image shown with the news item.
        from_date: ISO date string from which the item is displayed.
        to_date: ISO date string until which the item is displayed.
        active: Whether the news item is currently published.
    """

    id: int | None = None
    heading: str | None = None
    body: str | None = None
    image_url: str | None = None
    from_date: str | None = None
    to_date: str | None = None
    active: bool = True

    @classmethod
    def from_dict(cls, d: dict) -> NewsItemResponse:
        """Construct a NewsItemResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            heading=d.get("Heading"),
            body=d.get("Body"),
            image_url=d.get("ImageUrl"),
            from_date=d.get("From"),
            to_date=d.get("To"),
            active=d.get("Active", True),
        )

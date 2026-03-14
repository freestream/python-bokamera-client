"""
Resource namespace for homepage, news, and message template operations.

Exposes methods for retrieving and updating homepage settings, navigation
menus, gallery images, booking widget settings, news items, and message
template configurations.
"""

from __future__ import annotations

from uuid import UUID

from .._client import BokaMeraHTTPClient
from ..models.common import QueryResponse
from ..models.homepage import (
    HomepageImageResponse,
    HomepageMenuResponse,
    HomepageSettingsResponse,
    HomepageWidgetSettingsResponse,
    NewsItemResponse,
)


class HomepageResource:
    """Homepage operations: settings, images, widget configuration, news, and message templates."""

    def __init__(self, http: BokaMeraHTTPClient) -> None:
        self._http = http

    # ── Homepage settings ────────────────────────────────────────────────────

    def get_settings(self, *, site_path: str, company_id: UUID | str | None = None, **includes: bool) -> HomepageSettingsResponse:
        """Retrieve homepage settings for a company.

        Args:
            site_path: The company's site path (URL slug).
            company_id: Target company (defaults to the client's company).
            **includes: Boolean flags for optional related data (e.g. ``IncludeBookingSettings=True``).

        Returns:
            A :class:`~bokamera.models.homepage.HomepageSettingsResponse` for the company.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "SitePath": site_path,
            **includes,
        }
        return HomepageSettingsResponse.from_dict(self._http.get("/homepage/settings", params))

    def update_settings(self, *, company_id: UUID | str | None = None, **kwargs: object) -> HomepageSettingsResponse:
        """Update homepage settings for a company.

        Args:
            company_id: Target company (defaults to the client's company).
            **kwargs: Settings fields to update (e.g. ``HomepageName``, ``LogotypeUrl``).

        Returns:
            The updated :class:`~bokamera.models.homepage.HomepageSettingsResponse`.
        """
        body = {"CompanyId": str(company_id) if company_id else self._http.default_company_id, **kwargs}
        return HomepageSettingsResponse.from_dict(self._http.put("/homepage/settings", body))

    def get_menu(self, *, site_path: str, company_id: UUID | str | None = None) -> HomepageMenuResponse:
        """Retrieve the navigation menu for a company's homepage.

        Args:
            site_path: The company's site path (URL slug).
            company_id: Target company (defaults to the client's company).

        Returns:
            A :class:`~bokamera.models.homepage.HomepageMenuResponse` describing the menu structure.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "SitePath": site_path,
        }
        return HomepageMenuResponse.from_dict(self._http.get("/homepage/menu", params))

    # ── Homepage images ──────────────────────────────────────────────────────

    def list_images(self, *, site_path: str, company_id: UUID | str | None = None, id_: int | None = None) -> QueryResponse[HomepageImageResponse]:
        """List homepage gallery images for a company.

        Args:
            site_path: The company's site path (URL slug).
            company_id: Target company (defaults to the client's company).
            id_: Filter to a single image by ID.

        Returns:
            A paginated response of :class:`~bokamera.models.homepage.HomepageImageResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "SitePath": site_path,
            "Id": id_,
        }
        return QueryResponse.from_dict(self._http.get("/homepage/images", params), HomepageImageResponse)

    def create_image(
        self,
        *,
        image_url: str,
        title: str | None = None,
        description: str | None = None,
        company_id: UUID | str | None = None,
    ) -> HomepageImageResponse:
        """Add a new image to the homepage gallery.

        Args:
            image_url: URL of the image to add.
            title: Optional title displayed with the image.
            description: Optional description displayed with the image.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.homepage.HomepageImageResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "ImageUrl": image_url,
            "Title": title,
            "Description": description,
        }
        return HomepageImageResponse.from_dict(self._http.post("/homepage/images", body))

    def delete_image(self, image_id: int, *, company_id: UUID | str | None = None) -> HomepageImageResponse:
        """Remove an image from the homepage gallery.

        Args:
            image_id: ID of the image to delete.
            company_id: Target company (defaults to the client's company).

        Returns:
            The deleted :class:`~bokamera.models.homepage.HomepageImageResponse`.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return HomepageImageResponse.from_dict(self._http.delete(f"/homepage/images/{image_id}", params))

    # ── Widget settings ──────────────────────────────────────────────────────

    def get_widget_settings(self, *, site_path: str, company_id: UUID | str | None = None, **includes: bool) -> HomepageWidgetSettingsResponse:
        """Retrieve booking widget settings for a company.

        Args:
            site_path: The company's site path (URL slug).
            company_id: Target company (defaults to the client's company).
            **includes: Boolean flags for optional related data.

        Returns:
            A :class:`~bokamera.models.homepage.HomepageWidgetSettingsResponse`.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "SitePath": site_path,
            **includes,
        }
        return HomepageWidgetSettingsResponse.from_dict(self._http.get("/homepage/widget/settings", params))

    def update_widget_settings(
        self,
        *,
        company_id: UUID | str | None = None,
        service_layout_id: int | None = None,
        time_layout_id: int | None = None,
        booking_layout_id: int | None = None,
        primary_color: str | None = None,
        dark_theme: bool | None = None,
        show_service_image: bool | None = None,
        enable_login: bool | None = None,
        enable_direct_booking: bool | None = None,
    ) -> HomepageWidgetSettingsResponse:
        """Update booking widget settings for a company.

        Args:
            company_id: Target company (defaults to the client's company).
            service_layout_id: Layout ID for the service selection step.
            time_layout_id: Layout ID for the time selection step.
            booking_layout_id: Layout ID for the booking confirmation step.
            primary_color: Hex colour string for the widget's primary colour.
            dark_theme: When ``True``, enable the dark colour theme.
            show_service_image: When ``True``, display service images in the widget.
            enable_login: When ``True``, require login before booking.
            enable_direct_booking: When ``True``, skip confirmation step.

        Returns:
            The updated :class:`~bokamera.models.homepage.HomepageWidgetSettingsResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            **{k: v for k, v in {
                "ServiceLayoutId": service_layout_id,
                "TimeLayoutId": time_layout_id,
                "BookingLayoutId": booking_layout_id,
                "PrimaryColor": primary_color,
                "DarkTheme": dark_theme,
                "ShowServiceImage": show_service_image,
                "EnableLogin": enable_login,
                "EnableDirectBooking": enable_direct_booking,
            }.items() if v is not None},
        }
        return HomepageWidgetSettingsResponse.from_dict(self._http.put("/homepage/widget/settings", body))

    # ── News ─────────────────────────────────────────────────────────────────

    def list_news(
        self,
        *,
        site_path: str,
        company_id: UUID | str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        active: bool | None = None,
        plain_text: bool | None = None,
    ) -> QueryResponse[NewsItemResponse]:
        """List news items for a company's homepage.

        Args:
            site_path: The company's site path (URL slug).
            company_id: Target company (defaults to the client's company).
            from_date: ISO date string — return news published on or after this date.
            to_date: ISO date string — return news published on or before this date.
            active: When set, filter by active/inactive status.
            plain_text: When ``True``, strip HTML from the news body.

        Returns:
            A paginated response of :class:`~bokamera.models.homepage.NewsItemResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "SitePath": site_path,
            "From": from_date,
            "To": to_date,
            "Active": active,
            "PlainText": plain_text,
        }
        return QueryResponse.from_dict(self._http.get("/news", params), NewsItemResponse)

    def create_news(
        self,
        *,
        heading: str,
        body: str,
        image_url: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        company_id: UUID | str | None = None,
    ) -> NewsItemResponse:
        """Create a news item on a company's homepage.

        Args:
            heading: News item headline.
            body: News item body text (may include HTML).
            image_url: Optional URL of an image to display with the news item.
            from_date: ISO date string for when the item becomes visible.
            to_date: ISO date string for when the item stops being visible.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.homepage.NewsItemResponse`.
        """
        payload = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Heading": heading,
            "Body": body,
            "ImageUrl": image_url,
            "From": from_date,
            "To": to_date,
        }
        return NewsItemResponse.from_dict(self._http.post("/news", payload))

    def update_news(self, news_id: int, *, company_id: UUID | str | None = None, **kwargs: object) -> NewsItemResponse:
        """Update an existing news item.

        Args:
            news_id: ID of the news item to update.
            company_id: Target company (defaults to the client's company).
            **kwargs: News item fields to update (e.g. ``Heading``, ``Body``).

        Returns:
            The updated :class:`~bokamera.models.homepage.NewsItemResponse`.
        """
        body = {"CompanyId": str(company_id) if company_id else self._http.default_company_id, **kwargs}
        return NewsItemResponse.from_dict(self._http.put(f"/news/{news_id}", body))

    def delete_news(self, news_id: int, *, company_id: UUID | str | None = None) -> NewsItemResponse:
        """Delete a news item from a company's homepage.

        Args:
            news_id: ID of the news item to delete.
            company_id: Target company (defaults to the client's company).

        Returns:
            The deleted :class:`~bokamera.models.homepage.NewsItemResponse`.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return NewsItemResponse.from_dict(self._http.delete(f"/news/{news_id}", params))

    # ── Message templates ────────────────────────────────────────────────────

    def list_message_field_translations(self, *, group: str) -> list[dict]:
        """List available field translation tokens for message templates.

        Args:
            group: The template group to retrieve translations for (e.g. ``"Booking"``).

        Returns:
            A list of translation token dicts.
        """
        data = self._http.get("/messages/fieldtranslations", {"Group": group})
        if isinstance(data, list):
            return data
        return data.get("Results", [])

    def create_message_template(
        self,
        *,
        type_id: int,
        name: str,
        title: str | None = None,
        body: str | None = None,
        sender: str | None = None,
        language: str | None = None,
        services: list[dict] | None = None,
        company_id: UUID | str | None = None,
    ) -> dict:
        """Create a new message template.

        Args:
            type_id: ID of the message type (e.g. email confirmation, SMS reminder).
            name: Internal name for the template.
            title: Subject line or title of the message.
            body: Message body content (may include template tokens).
            sender: Sender name or email address.
            language: Language/locale code for the template (e.g. ``"sv"``).
            services: Services this template applies to.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict for the created template.
        """
        payload = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "TypeId": type_id,
            "Name": name,
            "Title": title,
            "Body": body,
            "Sender": sender,
            "Language": language,
            "Services": services or [],
        }
        return self._http.post("/messages/templates", payload)

    def update_message_template(self, template_id: int, *, company_id: UUID | str | None = None, **kwargs: object) -> dict:
        """Update an existing message template.

        Args:
            template_id: ID of the message template to update.
            company_id: Target company (defaults to the client's company).
            **kwargs: Template fields to update (e.g. ``Title``, ``Body``).

        Returns:
            Raw API response dict for the updated template.
        """
        body = {"CompanyId": str(company_id) if company_id else self._http.default_company_id, **kwargs}
        return self._http.put(f"/messages/templates/{template_id}", body)

    def delete_message_template(self, template_id: int, *, company_id: UUID | str | None = None) -> dict:
        """Delete a message template.

        Args:
            template_id: ID of the message template to delete.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict for the deletion.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return self._http.delete(f"/messages/templates/{template_id}", params)

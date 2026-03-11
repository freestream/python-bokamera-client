"""
Resource namespace for service operations.

Exposes methods for creating, listing, updating, and deleting services, as
well as managing service prices, resource type assignments, schedule
associations, available-time queries, and price calculations.
"""

from __future__ import annotations

from datetime import date, datetime
from uuid import UUID

from .._client import BokaMeraHTTPClient
from ..models.common import QueryResponse
from ..models.services import (
    AvailableTimesResponse,
    DurationTypeResponse,
    ServicePriceResponse,
    ServiceResponse,
    TotalPriceInformationResponse,
)


class ServiceResource:
    """Service operations: CRUD, pricing, scheduling, and availability."""

    def __init__(self, http: BokaMeraHTTPClient) -> None:
        self._http = http

    def list(
        self,
        *,
        company_id: UUID | str | None = None,
        id_: int | None = None,
        active: bool | None = None,
        include_resources: bool | None = None,
        include_schedules: bool | None = None,
        include_prices: bool | None = None,
        include_custom_fields: bool | None = None,
        include_rating_reviews: bool | None = None,
        price_date: date | None = None,
    ) -> list[ServiceResponse]:
        """List services for a company.

        Args:
            company_id: Target company (defaults to the client's company).
            id_: Filter to a single service by ID.
            active: When set, filter by active/inactive status.
            include_resources: Include resource type details in each service.
            include_schedules: Include schedule details in each service.
            include_prices: Include price details in each service.
            include_custom_fields: Include custom field definitions in each service.
            include_rating_reviews: Include rating review summary in each service.
            price_date: Evaluate prices as of this date.

        Returns:
            A list of :class:`~bokamera.models.services.ServiceResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Id": id_,
            "Active": active,
            "IncludeResources": include_resources,
            "IncludeSchedules": include_schedules,
            "IncludePrices": include_prices,
            "IncludeCustomFields": include_custom_fields,
            "IncludeRatingReviews": include_rating_reviews,
            "PriceDate": price_date.isoformat() if price_date else None,
        }
        data = self._http.get("/services", params)
        if isinstance(data, list):
            return [ServiceResponse.from_dict(d) for d in data]
        return [ServiceResponse.from_dict(d) for d in data.get("Results", [])]

    def create(
        self,
        *,
        name: str,
        description: str | None = None,
        group: str | None = None,
        active: bool = True,
        booking_status_id: int | None = None,
        duration: int | None = None,
        duration_type_id: int | None = None,
        total_spots: int | None = None,
        image_url: str | None = None,
        is_payment_enabled: bool = False,
        enable_booking_queue: bool = False,
        resource_types: list[dict] | None = None,
        schedules: list[dict] | None = None,
        custom_fields: list[dict] | None = None,
        company_id: UUID | str | None = None,
    ) -> ServiceResponse:
        """Create a new service.

        Args:
            name: Display name of the service.
            description: Optional description shown to customers.
            group: Optional group/category name for organising services.
            active: Whether the service is immediately active.
            booking_status_id: Default booking status applied to new bookings.
            duration: Duration of the service in minutes.
            duration_type_id: ID of the duration type (e.g. fixed, variable).
            total_spots: Maximum number of simultaneous bookings.
            image_url: URL to the service's cover image.
            is_payment_enabled: Enable payment collection for this service.
            enable_booking_queue: Enable the waiting queue for this service.
            resource_types: Resource type assignments for the service.
            schedules: Schedule assignments for the service.
            custom_fields: Custom field definitions for the service.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.services.ServiceResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Name": name,
            "Description": description,
            "Group": group,
            "Active": active,
            "BookingStatusId": booking_status_id,
            "Duration": duration,
            "DurationTypeId": duration_type_id,
            "TotalSpots": total_spots,
            "ImageUrl": image_url,
            "IsPaymentEnabled": is_payment_enabled,
            "EnableBookingQueue": enable_booking_queue,
            "ResourceTypes": resource_types or [],
            "Schedules": schedules or [],
            "CustomFields": custom_fields or [],
        }
        return ServiceResponse.from_dict(self._http.post("/services", body))

    def update(
        self,
        service_id: int,
        *,
        name: str | None = None,
        description: str | None = None,
        group: str | None = None,
        duration: int | None = None,
        total_spots: int | None = None,
        image_url: str | None = None,
        resource_types: list[dict] | None = None,
        schedules: list[dict] | None = None,
        custom_fields: list[dict] | None = None,
        company_id: UUID | str | None = None,
    ) -> ServiceResponse:
        """Update an existing service.

        Args:
            service_id: ID of the service to update.
            name: New display name.
            description: New description.
            group: New group/category name.
            duration: New duration in minutes.
            total_spots: New maximum number of simultaneous bookings.
            image_url: New cover image URL.
            resource_types: Updated resource type assignments.
            schedules: Updated schedule assignments.
            custom_fields: Updated custom field definitions.
            company_id: Target company (defaults to the client's company).

        Returns:
            The updated :class:`~bokamera.models.services.ServiceResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Name": name,
            "Description": description,
            "Group": group,
            "Duration": duration,
            "TotalSpots": total_spots,
            "ImageUrl": image_url,
            "ResourceTypes": resource_types,
            "Schedules": schedules,
            "CustomFields": custom_fields,
        }
        return ServiceResponse.from_dict(self._http.put(f"/services/{service_id}", body))

    def delete(self, service_id: int, *, company_id: UUID | str | None = None) -> ServiceResponse:
        """Delete a service.

        Args:
            service_id: ID of the service to delete.
            company_id: Target company (defaults to the client's company).

        Returns:
            The deleted :class:`~bokamera.models.services.ServiceResponse`.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return ServiceResponse.from_dict(self._http.delete(f"/services/{service_id}", params))

    def list_grouped(self, *, company_id: UUID | str | None = None, active: bool | None = None) -> list[dict]:
        """List services grouped by their group/category name.

        Args:
            company_id: Target company (defaults to the client's company).
            active: When set, filter to active or inactive services only.

        Returns:
            Raw API response list of grouped service dicts.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Active": active,
        }
        return self._http.get("/services/grouped", params)

    def list_duration_types(self) -> list[DurationTypeResponse]:
        """List all available service duration types.

        Returns:
            A list of :class:`~bokamera.models.services.DurationTypeResponse` objects.
        """
        data = self._http.get("/services/durationtypes")
        if isinstance(data, list):
            return [DurationTypeResponse.from_dict(d) for d in data]
        return [DurationTypeResponse.from_dict(d) for d in data.get("Results", [])]

    def calculate_price(
        self,
        service_id: int,
        *,
        interval: dict | None = None,
        rebate_code_ids: list[int] | None = None,
        article_ids: list[int] | None = None,
        quantities: list[dict] | None = None,
        customer_email: str | None = None,
        booking_id: int | None = None,
        company_id: UUID | str | None = None,
    ) -> TotalPriceInformationResponse:
        """Calculate the total price for booking a service.

        Args:
            service_id: ID of the service to price.
            interval: Time interval dict with ``From`` and ``To`` keys.
            rebate_code_ids: IDs of rebate codes to apply.
            article_ids: IDs of additional articles (add-ons) to include.
            quantities: Quantity lines to include in the price calculation.
            customer_email: Customer email, used for customer-specific pricing rules.
            booking_id: Existing booking ID when recalculating for an update.
            company_id: Target company (defaults to the client's company).

        Returns:
            A :class:`~bokamera.models.services.TotalPriceInformationResponse` with the calculated totals.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Interval": interval,
            "RebateCodeIds": rebate_code_ids,
            "ArticleIds": article_ids,
            "Quantities": quantities,
            "CustomerEmail": customer_email,
            "BookingId": booking_id,
        }
        return TotalPriceInformationResponse.from_dict(self._http.put(f"/services/{service_id}/calculateprice", body))

    def add_resource_type(self, service_id: int, *, resource_types: list[dict]) -> ServiceResponse:
        """Assign one or more resource types to a service.

        Args:
            service_id: ID of the service to modify.
            resource_types: List of resource type assignment dicts.

        Returns:
            The updated :class:`~bokamera.models.services.ServiceResponse`.
        """
        body = {"ResourceTypes": resource_types}
        return ServiceResponse.from_dict(self._http.post(f"/services/{service_id}/addresourcetype", body))

    def remove_resource_type(self, service_id: int, resource_type_id: int, *, company_id: UUID | str | None = None) -> ServiceResponse:
        """Remove a resource type assignment from a service.

        Args:
            service_id: ID of the service to modify.
            resource_type_id: ID of the resource type to remove.
            company_id: Target company (defaults to the client's company).

        Returns:
            The updated :class:`~bokamera.models.services.ServiceResponse`.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return ServiceResponse.from_dict(self._http.delete(f"/services/{service_id}/resourcetypes/{resource_type_id}", params))

    def remove_date_schedule(self, service_id: int, date_schedule_id: int, *, company_id: UUID | str | None = None) -> ServiceResponse:
        """Remove a date schedule association from a service.

        Args:
            service_id: ID of the service to modify.
            date_schedule_id: ID of the date schedule to remove.
            company_id: Target company (defaults to the client's company).

        Returns:
            The updated :class:`~bokamera.models.services.ServiceResponse`.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return ServiceResponse.from_dict(self._http.delete(f"/services/{service_id}/dateschedules/{date_schedule_id}", params))

    def remove_recurring_schedule(self, service_id: int, recurring_schedule_id: int, *, company_id: UUID | str | None = None) -> ServiceResponse:
        """Remove a recurring schedule association from a service.

        Args:
            service_id: ID of the service to modify.
            recurring_schedule_id: ID of the recurring schedule to remove.
            company_id: Target company (defaults to the client's company).

        Returns:
            The updated :class:`~bokamera.models.services.ServiceResponse`.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return ServiceResponse.from_dict(self._http.delete(f"/services/{service_id}/recurringschedules/{recurring_schedule_id}", params))

    def get_available_times(
        self,
        service_id: int,
        *,
        from_: datetime,
        to: datetime,
        resources: list[dict] | None = None,
        number_of_resources: int | None = None,
        show_per_resource: bool | None = None,
        inside_search_interval: bool | None = None,
        duration: int | None = None,
        article_ids: list[int] | None = None,
        company_id: UUID | str | None = None,
    ) -> AvailableTimesResponse:
        """Retrieve available time slots for a service within a date range.

        Args:
            service_id: ID of the service to query.
            from_: Start of the search window.
            to: End of the search window.
            resources: Restrict to specific resources per resource type.
                Each entry is a dict with ``ResourceTypeId`` (int) and ``ResourceId`` (int).
            number_of_resources: Number of resources to book per resource type (default 1).
            show_per_resource: When ``True``, return availability broken down per resource.
            inside_search_interval: When ``True``, both start and end time must fall inside the
                search interval (default ``False`` — only start time needs to be inside).
            duration: Duration to book in minutes; must be within the service's min/max range.
            article_ids: Article IDs to include when checking slot availability.
            company_id: Target company (defaults to the client's company).

        Returns:
            An :class:`~bokamera.models.services.AvailableTimesResponse` with the available slots.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "From": from_.isoformat(),
            "To": to.isoformat(),
            "Resources": resources,
            "NumberOfResources": number_of_resources,
            "ShowPerResource": show_per_resource,
            "InsideSearchInterval": inside_search_interval,
            "Duration": duration,
            "ArticleIds": article_ids,
        }
        return AvailableTimesResponse.from_dict(self._http.get(f"/services/{service_id}/availabletimes", params))

    def get_next_free_time(
        self,
        service_id: int,
        *,
        from_: datetime,
        to: datetime,
        resources: list[dict] | None = None,
        number_of_resources: int | None = None,
        show_per_resource: bool | None = None,
        duration: int | None = None,
        article_ids: list[int] | None = None,
        company_id: UUID | str | None = None,
    ) -> AvailableTimesResponse:
        """Find the next available time slot for a service from a given start datetime.

        Args:
            service_id: ID of the service to query.
            from_: Start of the search window.
            to: End of the search window (optional; defaults to one year ahead if omitted).
            resources: Restrict to specific resources per resource type.
                Each entry is a dict with ``ResourceTypeId`` (int) and ``ResourceId`` (int).
            number_of_resources: Number of resources to book per resource type (default 1).
            show_per_resource: When ``True``, return availability broken down per resource.
            duration: Duration to book in minutes; must be within the service's min/max range.
            article_ids: Article IDs to include when checking slot availability.
            company_id: Target company (defaults to the client's company).

        Returns:
            An :class:`~bokamera.models.services.AvailableTimesResponse` with the next free slot.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "From": from_.isoformat(),
            "To": to.isoformat(),
            "Resources": resources,
            "NumberOfResources": number_of_resources,
            "ShowPerResource": show_per_resource,
            "Duration": duration,
            "ArticleIds": article_ids,
        }
        return AvailableTimesResponse.from_dict(self._http.get(f"/services/{service_id}/nextfreetime", params))

    def get_available_times_grouped(
        self,
        service_id: int,
        *,
        from_: datetime,
        to: datetime,
        resources: list[dict] | None = None,
        number_of_resources: int | None = None,
        company_id: UUID | str | None = None,
    ) -> dict:
        """Retrieve available time slots for a service grouped by date.

        Args:
            service_id: ID of the service to query.
            from_: Start of the search window.
            to: End of the search window.
            resources: Restrict to specific resources per resource type.
                Each entry is a dict with ``ResourceTypeId`` (int) and ``ResourceId`` (int).
            number_of_resources: Number of resources to book per resource type (default 1).
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict with available times grouped by date.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "From": from_.isoformat(),
            "To": to.isoformat(),
            "Resources": resources,
            "NumberOfResources": number_of_resources,
        }
        return self._http.get(f"/services/{service_id}/availabletimes/grouped", params)

    # ── Service prices ───────────────────────────────────────────────────────

    def create_price(
        self,
        *,
        service_id: int,
        price: float,
        currency_id: str,
        vat: float | None = None,
        calculation_type_id: int | None = None,
        category: str | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
        days_of_week: list[int] | None = None,
        from_time: str | None = None,
        to_time: str | None = None,
        company_id: UUID | str | None = None,
    ) -> ServicePriceResponse:
        """Create a new price rule for a service.

        Args:
            service_id: ID of the service this price applies to.
            price: Base price amount.
            currency_id: ISO currency code (e.g. ``"SEK"``).
            vat: VAT amount or percentage.
            calculation_type_id: ID of the price calculation type.
            category: Optional price category label.
            from_date: Start date from which this price is valid.
            to_date: End date until which this price is valid.
            days_of_week: Days of the week this price applies to (0 = Monday).
            from_time: Start of the daily time window (``"HH:MM"`` string).
            to_time: End of the daily time window (``"HH:MM"`` string).
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.services.ServicePriceResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "ServiceId": service_id,
            "Price": price,
            "CurrencyId": currency_id,
            "VAT": vat,
            "CalculationTypeId": calculation_type_id,
            "Category": category,
            "From": from_date.isoformat() if from_date else None,
            "To": to_date.isoformat() if to_date else None,
            "DaysOfWeek": days_of_week,
            "FromTime": from_time,
            "ToTime": to_time,
        }
        return ServicePriceResponse.from_dict(self._http.post("/services/prices/", body))

    def update_price(self, price_id: int, *, company_id: UUID | str | None = None, **kwargs: object) -> ServicePriceResponse:
        """Update an existing service price rule.

        Args:
            price_id: ID of the price rule to update.
            company_id: Target company (defaults to the client's company).
            **kwargs: Price fields to update (e.g. ``Price``, ``VAT``, ``From``, ``To``).

        Returns:
            The updated :class:`~bokamera.models.services.ServicePriceResponse`.
        """
        body = {"CompanyId": str(company_id) if company_id else self._http.default_company_id, **kwargs}
        return ServicePriceResponse.from_dict(self._http.put(f"/services/prices/{price_id}", body))

    def delete_price(self, price_id: int, *, company_id: UUID | str | None = None) -> ServicePriceResponse:
        """Delete a service price rule.

        Args:
            price_id: ID of the price rule to delete.
            company_id: Target company (defaults to the client's company).

        Returns:
            The deleted :class:`~bokamera.models.services.ServicePriceResponse`.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return ServicePriceResponse.from_dict(self._http.delete(f"/services/prices/{price_id}", params))

    def delete_price_mapping(self, mapping_id: UUID | str, *, company_id: UUID | str | None = None) -> dict:
        """Delete a service price mapping.

        Args:
            mapping_id: UUID of the price mapping to delete.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict for the deletion.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return self._http.delete(f"/services/prices/mappings/{mapping_id}", params)

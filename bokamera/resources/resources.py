"""
Resource namespace for resource and time-exception operations.

Exposes methods for creating, listing, updating, and deleting resources and
resource types, as well as managing time exceptions (blocks/closures) and
checking for booking collisions.
"""

from __future__ import annotations

from datetime import date, datetime, time
from uuid import UUID

from .._client import BokaMeraHTTPClient
from ..models.resources import (
    CollidingBookingResponse,
    ResourceResponse,
    ResourceTimeExceptionResponse,
    ResourceTypeResponse,
)


class ResourceResource:
    """Resource operations: CRUD for resources, resource types, and time exceptions."""

    def __init__(self, http: BokaMeraHTTPClient) -> None:
        self._http = http

    # ── Resources ────────────────────────────────────────────────────────────

    def list(
        self,
        *,
        company_id: UUID | str | None = None,
        id_: int | None = None,
        active: bool | None = None,
        include_exceptions: bool | None = None,
        exceptions_from: date | None = None,
        exceptions_to: date | None = None,
        include_bookings: bool | None = None,
        bookings_from: date | None = None,
        bookings_to: date | None = None,
    ) -> list[ResourceResponse]:
        """List resources for a company.

        Args:
            company_id: Target company (defaults to the client's company).
            id_: Filter to a single resource by ID.
            active: When set, filter by active/inactive status.
            include_exceptions: Include time exception details in each resource.
            exceptions_from: Start of the date range for included exceptions.
            exceptions_to: End of the date range for included exceptions.
            include_bookings: Include booking details in each resource.
            bookings_from: Start of the date range for included bookings.
            bookings_to: End of the date range for included bookings.

        Returns:
            A list of :class:`~bokamera.models.resources.ResourceResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Id": id_,
            "Active": active,
            "IncludeExceptions": include_exceptions,
            "ExceptionsQueryFromDate": exceptions_from.isoformat() if exceptions_from else None,
            "ExceptionsQueryToDate": exceptions_to.isoformat() if exceptions_to else None,
            "IncludeBookings": include_bookings,
            "BookingsQueryFromDate": bookings_from.isoformat() if bookings_from else None,
            "BookingsQueryToDate": bookings_to.isoformat() if bookings_to else None,
        }
        data = self._http.get("/resource", params)
        if isinstance(data, list):
            return [ResourceResponse.from_dict(d) for d in data]
        return [ResourceResponse.from_dict(d) for d in data.get("Results", [])]

    def create(
        self,
        *,
        name: str,
        description: str | None = None,
        active: bool = True,
        color: str | None = None,
        email: str | None = None,
        mobile_phone: str | None = None,
        access_group: str | None = None,
        email_notification: bool = False,
        sms_notification: bool = False,
        send_email_reminder: bool = False,
        send_sms_reminder: bool = False,
        image_url: str | None = None,
        custom_fields: list[dict] | None = None,
        company_id: UUID | str | None = None,
    ) -> ResourceResponse:
        """Create a new resource.

        Args:
            name: Display name of the resource.
            description: Optional description of the resource.
            active: Whether the resource is immediately available for bookings.
            color: Hex colour string used in calendar views.
            email: Email address of the resource (e.g. a staff member).
            mobile_phone: Mobile phone number of the resource.
            access_group: Optional access control group name.
            email_notification: Send email notifications to this resource.
            sms_notification: Send SMS notifications to this resource.
            send_email_reminder: Send email reminders to this resource.
            send_sms_reminder: Send SMS reminders to this resource.
            image_url: URL to the resource's profile image.
            custom_fields: Custom field values for the resource.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.resources.ResourceResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Name": name,
            "Description": description,
            "Active": active,
            "Color": color,
            "Email": email,
            "MobilePhone": mobile_phone,
            "AccessGroup": access_group,
            "EmailNotification": email_notification,
            "SMSNotification": sms_notification,
            "SendEmailReminder": send_email_reminder,
            "SendSMSReminder": send_sms_reminder,
            "ImageUrl": image_url,
            "CustomFields": custom_fields or [],
        }
        return ResourceResponse.from_dict(self._http.post("/resource", body))

    def update(self, resource_id: int, *, company_id: UUID | str | None = None, **kwargs: object) -> ResourceResponse:
        """Update an existing resource.

        Args:
            resource_id: ID of the resource to update.
            company_id: Target company (defaults to the client's company).
            **kwargs: Resource fields to update (e.g. ``Name``, ``Color``, ``Active``).

        Returns:
            The updated :class:`~bokamera.models.resources.ResourceResponse`.
        """
        body = {"CompanyId": str(company_id) if company_id else self._http.default_company_id, **kwargs}
        return ResourceResponse.from_dict(self._http.put(f"/resource/{resource_id}", body))

    def delete(self, resource_id: int, *, force: bool = False, company_id: UUID | str | None = None) -> ResourceResponse:
        """Delete a resource.

        Args:
            resource_id: ID of the resource to delete.
            force: When ``True``, delete even if the resource has existing bookings.
            company_id: Target company (defaults to the client's company).

        Returns:
            The deleted :class:`~bokamera.models.resources.ResourceResponse`.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Force": force,
        }
        return ResourceResponse.from_dict(self._http.delete(f"/resource/{resource_id}", params))

    # ── Resource types ───────────────────────────────────────────────────────

    def list_types(
        self,
        *,
        company_id: UUID | str | None = None,
        id_: int | None = None,
        active: bool | None = None,
        include_resources: bool | None = None,
    ) -> list[ResourceTypeResponse]:
        """List resource types for a company.

        Args:
            company_id: Target company (defaults to the client's company).
            id_: Filter to a single resource type by ID.
            active: When set, filter by active/inactive status.
            include_resources: Include the resources belonging to each type.

        Returns:
            A list of :class:`~bokamera.models.resources.ResourceTypeResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Id": id_,
            "Active": active,
            "IncludeResources": include_resources,
        }
        data = self._http.get("/resourcetypes", params)
        if isinstance(data, list):
            return [ResourceTypeResponse.from_dict(d) for d in data]
        return [ResourceTypeResponse.from_dict(d) for d in data.get("Results", [])]

    def create_type(
        self,
        *,
        name: str,
        description: str | None = None,
        active: bool = True,
        resources: list[dict] | None = None,
        company_id: UUID | str | None = None,
    ) -> ResourceTypeResponse:
        """Create a new resource type.

        Args:
            name: Display name of the resource type.
            description: Optional description of the resource type.
            active: Whether the type is immediately active.
            resources: Initial list of resources to assign to this type.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.resources.ResourceTypeResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Name": name,
            "Description": description,
            "Active": active,
            "Resources": resources or [],
        }
        return ResourceTypeResponse.from_dict(self._http.post("/resourcetypes", body))

    def update_type(self, type_id: int, *, company_id: UUID | str | None = None, **kwargs: object) -> ResourceTypeResponse:
        """Update an existing resource type.

        Args:
            type_id: ID of the resource type to update.
            company_id: Target company (defaults to the client's company).
            **kwargs: Resource type fields to update (e.g. ``Name``, ``Active``).

        Returns:
            The updated :class:`~bokamera.models.resources.ResourceTypeResponse`.
        """
        body = {"CompanyId": str(company_id) if company_id else self._http.default_company_id, **kwargs}
        return ResourceTypeResponse.from_dict(self._http.put(f"/resourcetypes/{type_id}", body))

    def delete_type(self, type_id: int, *, company_id: UUID | str | None = None) -> dict:
        """Delete a resource type.

        Args:
            type_id: ID of the resource type to delete.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict for the deletion.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return self._http.delete(f"/resourcetypes/{type_id}", params)

    # ── Time exceptions ──────────────────────────────────────────────────────

    def list_exceptions(
        self,
        *,
        company_id: UUID | str | None = None,
        resource_ids: list[int] | None = None,
        start: datetime | None = None,
        end: datetime | None = None,
        is_recurring: bool | None = None,
        is_blocking: bool | None = None,
        include_resource_details: bool | None = None,
        max_limit: int | None = None,
        include_calendar_export_status: bool | None = None,
    ) -> list[ResourceTimeExceptionResponse]:
        """List time exceptions (blocks/closures) for resources.

        Args:
            company_id: Target company (defaults to the client's company).
            resource_ids: Filter to exceptions for these resource IDs.
            start: Return exceptions starting on or after this datetime.
            end: Return exceptions starting on or before this datetime.
            is_recurring: Filter to recurring or one-off exceptions.
            is_blocking: Filter to blocking or non-blocking exceptions.
            include_resource_details: Include resource info in each exception.
            max_limit: Maximum number of exceptions to return.

        Returns:
            A list of :class:`~bokamera.models.resources.ResourceTimeExceptionResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "ResourceIds": resource_ids,
            "TimeExceptionStart": start.isoformat() if start else None,
            "TimeExceptionEnd": end.isoformat() if end else None,
            "IsRecurring": is_recurring,
            "IsBlocking": is_blocking,
            "IncludeResourceDetails": include_resource_details,
            "MaxLimit": max_limit,
            "IncludeCalendarExportStatus": include_calendar_export_status,
        }
        data = self._http.get("/timeexceptions", params)
        if isinstance(data, list):
            return [ResourceTimeExceptionResponse.from_dict(d) for d in data]
        return [ResourceTimeExceptionResponse.from_dict(d) for d in data.get("Results", [])]

    def create_exception(
        self,
        *,
        from_: datetime,
        to: datetime,
        resource_ids: list[int],
        from_time: time | None = None,
        to_time: time | None = None,
        days_of_week: list[int] | None = None,
        reason_text: str | None = None,
        reason_text_public: str | None = None,
        color: str | None = None,
        block_time: bool = True,
        private: bool = False,
        force: bool = False,
        send_sms_confirmation: bool = False,
        send_email_confirmation: bool = False,
        cancel_message: str | None = None,
        colliding_booking_options: str | None = None,
        company_id: UUID | str | None = None,
    ) -> ResourceTimeExceptionResponse:
        """Create a time exception (block/closure) for one or more resources.

        Args:
            from_: Start datetime of the exception period.
            to: End datetime of the exception period.
            resource_ids: IDs of the resources to apply the exception to.
            from_time: Daily start time for recurring exceptions.
            to_time: Daily end time for recurring exceptions.
            days_of_week: Days of the week the exception recurs on (0 = Monday).
            reason_text: Internal reason text for the exception.
            reason_text_public: Public-facing reason text shown to customers.
            color: Hex colour string for calendar display.
            block_time: When ``True``, the exception blocks new bookings.
            private: When ``True``, the exception is hidden from customers.
            force: When ``True``, create the exception even if bookings exist.
            send_sms_confirmation: Send SMS cancellation notices to affected customers.
            send_email_confirmation: Send email cancellation notices to affected customers.
            cancel_message: Custom message included in cancellation notifications.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.resources.ResourceTimeExceptionResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "From": from_.isoformat(),
            "To": to.isoformat(),
            "ResourceIds": resource_ids,
            "FromTime": from_time.isoformat() if from_time else None,
            "ToTime": to_time.isoformat() if to_time else None,
            "DaysOfWeek": days_of_week,
            "ReasonText": reason_text,
            "ReasonTextPublic": reason_text_public,
            "Color": color,
            "BlockTime": block_time,
            "Private": private,
            "Force": force,
            "SendSmsConfirmation": send_sms_confirmation,
            "SendEmailConfirmation": send_email_confirmation,
            "CancelMessage": cancel_message,
            "CollidingBookingOptions": colliding_booking_options,
        }
        return ResourceTimeExceptionResponse.from_dict(self._http.post("/timeexceptions", body))

    def update_exception(self, exception_id: int, *, company_id: UUID | str | None = None, **kwargs: object) -> ResourceTimeExceptionResponse:
        """Update an existing time exception.

        Args:
            exception_id: ID of the time exception to update.
            company_id: Target company (defaults to the client's company).
            **kwargs: Exception fields to update (e.g. ``ReasonText``, ``BlockTime``).

        Returns:
            The updated :class:`~bokamera.models.resources.ResourceTimeExceptionResponse`.
        """
        body = {"CompanyId": str(company_id) if company_id else self._http.default_company_id, **kwargs}
        return ResourceTimeExceptionResponse.from_dict(self._http.put(f"/timeexceptions/{exception_id}", body))

    def delete_exception(self, exception_id: int, *, company_id: UUID | str | None = None) -> ResourceTimeExceptionResponse:
        """Delete a time exception.

        Args:
            exception_id: ID of the time exception to delete.
            company_id: Target company (defaults to the client's company).

        Returns:
            The deleted :class:`~bokamera.models.resources.ResourceTimeExceptionResponse`.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return ResourceTimeExceptionResponse.from_dict(self._http.delete(f"/timeexceptions/{exception_id}", params))

    def get_colliding_events(
        self,
        *,
        resource_ids: list[int],
        from_: datetime,
        to: datetime,
        from_time: time | None = None,
        to_time: time | None = None,
        days_of_week: list[int] | None = None,
        include_service_information: bool | None = None,
        include_customer_information: bool | None = None,
        company_id: UUID | str | None = None,
    ) -> CollidingBookingResponse:
        """Find bookings that would collide with a proposed time exception.

        Args:
            resource_ids: IDs of the resources to check for collisions.
            from_: Start of the proposed exception period.
            to: End of the proposed exception period.
            from_time: Daily start time for recurring exception windows.
            to_time: Daily end time for recurring exception windows.
            days_of_week: Days of the week for recurring exception windows.
            include_service_information: Include service details in each colliding booking.
            include_customer_information: Include customer details in each colliding booking.
            company_id: Target company (defaults to the client's company).

        Returns:
            A :class:`~bokamera.models.resources.CollidingBookingResponse` listing any conflicting bookings.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "ResourceIds": resource_ids,
            "From": from_.isoformat(),
            "To": to.isoformat(),
            "FromTime": from_time.isoformat() if from_time else None,
            "ToTime": to_time.isoformat() if to_time else None,
            "DaysOfWeek": days_of_week,
            "IncludeServiceInformation": include_service_information,
            "IncludeCustomerInformation": include_customer_information,
        }
        return CollidingBookingResponse.from_dict(self._http.get("/timeexceptions/collidingevents", params))

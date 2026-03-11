"""
Resource namespace for booking operations.

Exposes methods for creating, listing, updating, deleting, and managing
bookings, as well as booking log entries, the user waiting queue, printout
templates, and booking reports.
"""

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from .._client import BokaMeraHTTPClient
from ..models.bookings import (
    BookingLogResponse,
    BookingQuantity,
    BookingResponse,
    BookingStatusResponse,
    BookingUserQueueResponse,
    GroupedBookingResponse,
    PaymentOption,
    PrintoutResponse,
    ReportResponse,
    SendReceiptMethod,
)
from ..models.common import CustomFieldValue, QueryResponse


class BookingResource:
    """Booking operations: CRUD, approval, payment, queue, log, and reports."""

    def __init__(self, http: BokaMeraHTTPClient) -> None:
        self._http = http

    # ── Bookings ────────────────────────────────────────────────────────────

    def list(
        self,
        *,
        company_id: UUID | str | None = None,
        service_ids: list[int] | None = None,
        status_ids: list[int] | None = None,
        customer_id: UUID | str | None = None,
        booking_start: datetime | None = None,
        booking_end: datetime | None = None,
        company_bookings: bool | None = None,
        include_resources: bool | None = None,
        include_custom_fields: bool | None = None,
        include_payment_log: bool | None = None,
        skip: int | None = None,
        take: int | None = None,
    ) -> QueryResponse[BookingResponse]:
        """List bookings with optional filters.

        Args:
            company_id: Filter to a specific company (defaults to the client's company).
            service_ids: Filter to bookings for these service IDs.
            status_ids: Filter to bookings with these status IDs.
            customer_id: Filter to bookings by this customer.
            booking_start: Return bookings starting on or after this datetime.
            booking_end: Return bookings starting on or before this datetime.
            company_bookings: When ``True``, return all company bookings regardless of user.
            include_resources: Include resource details in each booking.
            include_custom_fields: Include custom field values in each booking.
            include_payment_log: Include payment log entries in each booking.
            skip: Number of results to skip (for pagination).
            take: Maximum number of results to return.

        Returns:
            A paginated :class:`~bokamera.models.common.QueryResponse` of bookings.
        """
        params: dict = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "StatusIds": service_ids,
            "ServiceIds": service_ids,
            "CustomerId": str(customer_id) if customer_id else None,
            "BookingStart": booking_start.isoformat() if booking_start else None,
            "BookingEnd": booking_end.isoformat() if booking_end else None,
            "CompanyBookings": company_bookings,
            "IncludeResources": include_resources,
            "IncludeCustomFields": include_custom_fields,
            "IncludePaymentLog": include_payment_log,
            "Skip": skip,
            "Take": take,
        }
        data = self._http.get("/bookings", params)
        return QueryResponse.from_dict(data, BookingResponse)

    def create(
        self,
        *,
        from_: datetime,
        to: datetime,
        service_id: int,
        quantities: list[dict] | None = None,
        customer: dict | None = None,
        resources: list[dict] | None = None,
        articles: list[dict] | None = None,
        company_id: UUID | str | None = None,
        customer_id: UUID | str | None = None,
        send_email_confirmation: bool = True,
        send_sms_confirmation: bool = False,
        payment_option: PaymentOption = PaymentOption.DEFAULT_SETTING,
        custom_fields: list[dict] | None = None,
        rebate_code_ids: list[int] | None = None,
    ) -> BookingResponse:
        """Create a new booking.

        Args:
            from_: Start datetime of the booking.
            to: End datetime of the booking.
            service_id: ID of the service to book.
            quantities: Quantity lines (e.g. ``[{"Id": 1, "Quantity": 2}]``).
            customer: Customer details dict (``Firstname``, ``Lastname``, ``Email``, ``Phone``).
            resources: Resource assignments for the booking.
            articles: Articles (e.g. add-ons) to attach to the booking.
            company_id: Target company (defaults to the client's company).
            customer_id: UUID of an existing customer to link to the booking.
            send_email_confirmation: Send an email confirmation to the customer.
            send_sms_confirmation: Send an SMS confirmation to the customer.
            payment_option: Payment handling behaviour for this booking.
            custom_fields: Custom field values collected at booking time.
            rebate_code_ids: IDs of rebate codes to apply.

        Returns:
            The created :class:`~bokamera.models.bookings.BookingResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "From": from_.isoformat(),
            "To": to.isoformat(),
            "ServiceId": service_id,
            "Quantities": quantities or [],
            "Customer": customer,
            "Resources": resources or [],
            "Articles": articles or [],
            "CustomerId": str(customer_id) if customer_id else None,
            "SendEmailConfirmation": send_email_confirmation,
            "SendSmsConfirmation": send_sms_confirmation,
            "PaymentOption": int(payment_option),
            "CustomFields": custom_fields or [],
            "RebateCodeIds": rebate_code_ids or [],
        }
        return BookingResponse.from_dict(self._http.post("/bookings", body))

    def update(
        self,
        booking_id: int,
        *,
        company_id: UUID | str | None = None,
        unbooked_comments: str | None = None,
        resources: list[dict] | None = None,
        custom_fields: list[dict] | None = None,
    ) -> BookingResponse:
        """Update an existing booking.

        Args:
            booking_id: ID of the booking to update.
            company_id: Target company (defaults to the client's company).
            unbooked_comments: Internal comment to store on the booking.
            resources: Updated resource assignments.
            custom_fields: Updated custom field values.

        Returns:
            The updated :class:`~bokamera.models.bookings.BookingResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "UnbookedComments": unbooked_comments,
            "Resources": resources,
            "CustomFields": custom_fields,
        }
        return BookingResponse.from_dict(self._http.put(f"/bookings/{booking_id}", body))

    def delete(
        self,
        booking_id: int,
        *,
        unbooked_comments: str | None = None,
        message: str | None = None,
        send_sms_confirmation: bool | None = None,
        send_email_confirmation: bool | None = None,
    ) -> BookingResponse:
        """Cancel / delete a booking.

        Args:
            booking_id: ID of the booking to cancel.
            unbooked_comments: Reason for cancellation stored on the booking.
            message: Custom message included in the cancellation notification.
            send_sms_confirmation: Send an SMS cancellation notification.
            send_email_confirmation: Send an email cancellation notification.

        Returns:
            The cancelled :class:`~bokamera.models.bookings.BookingResponse`.
        """
        params = {
            "UnBookedComments": unbooked_comments,
            "Message": message,
            "SendSmsConfirmation": send_sms_confirmation,
            "SendEmailConfirmation": send_email_confirmation,
        }
        return BookingResponse.from_dict(self._http.delete(f"/bookings/{booking_id}", params))

    def delete_by_code(self, booking_id: int, cancellation_code: str) -> BookingResponse:
        """Cancel a booking using the self-service cancellation code.

        Args:
            booking_id: ID of the booking to cancel.
            cancellation_code: The cancellation code provided to the customer.

        Returns:
            The cancelled :class:`~bokamera.models.bookings.BookingResponse`.
        """
        return BookingResponse.from_dict(
            self._http.delete(f"/bookings/deletebycode/{booking_id}", {"CancellationCode": cancellation_code})
        )

    def create_repeat(
        self,
        *,
        dates_to_repeat: list[str],
        service_id: int,
        customer: dict | None = None,
        resources: list[dict] | None = None,
        quantities: list[dict] | None = None,
        company_id: UUID | str | None = None,
    ) -> dict:
        """Create identical bookings across multiple dates (repeat booking).

        Args:
            dates_to_repeat: ISO date/datetime strings for each occurrence.
            service_id: ID of the service to book on each date.
            customer: Customer details dict.
            resources: Resource assignments for each occurrence.
            quantities: Quantity lines applied to each occurrence.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict containing the created bookings.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "DatesToRepeat": dates_to_repeat,
            "ServiceId": service_id,
            "Customer": customer,
            "Resources": resources or [],
            "Quantities": quantities or [],
        }
        return self._http.post("/bookings/repeat", body)

    def list_grouped(
        self,
        *,
        company_id: UUID | str | None = None,
        booking_start: datetime | None = None,
        booking_end: datetime | None = None,
        company_bookings: bool | None = None,
        skip: int | None = None,
        take: int | None = None,
    ) -> QueryResponse[GroupedBookingResponse]:
        """List bookings grouped by calendar date.

        Args:
            company_id: Target company (defaults to the client's company).
            booking_start: Return bookings on or after this datetime.
            booking_end: Return bookings on or before this datetime.
            company_bookings: Include all company bookings regardless of user.
            skip: Pagination offset.
            take: Maximum results to return.

        Returns:
            A paginated response of :class:`~bokamera.models.bookings.GroupedBookingResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "BookingStart": booking_start.isoformat() if booking_start else None,
            "BookingEnd": booking_end.isoformat() if booking_end else None,
            "CompanyBookings": company_bookings,
            "Skip": skip,
            "Take": take,
        }
        data = self._http.get("/bookings/grouped", params)
        return QueryResponse.from_dict(data, GroupedBookingResponse)

    def list_statuses(self) -> QueryResponse[BookingStatusResponse]:
        """List all available booking status options.

        Returns:
            A paginated response of :class:`~bokamera.models.bookings.BookingStatusResponse` objects.
        """
        return QueryResponse.from_dict(self._http.get("/bookings/status"), BookingStatusResponse)

    def approve(self, booking_id: int, *, payment_option: PaymentOption = PaymentOption.DEFAULT_SETTING) -> BookingResponse:
        """Approve a pending booking.

        Args:
            booking_id: ID of the booking to approve.
            payment_option: Payment handling behaviour applied on approval.

        Returns:
            The updated :class:`~bokamera.models.bookings.BookingResponse`.
        """
        return BookingResponse.from_dict(
            self._http.put(f"/bookings/{booking_id}/approve", {"PaymentOption": int(payment_option)})
        )

    def decline(self, booking_id: int, *, comment: str | None = None, message: str | None = None) -> BookingResponse:
        """Decline a pending booking.

        Args:
            booking_id: ID of the booking to decline.
            comment: Internal comment stored on the booking record.
            message: Custom message sent to the customer in the decline notification.

        Returns:
            The updated :class:`~bokamera.models.bookings.BookingResponse`.
        """
        return BookingResponse.from_dict(
            self._http.put(f"/bookings/{booking_id}/decline", {"Comment": comment, "Message": message})
        )

    def mark_as_paid(self, booking_id: int, *, comment: str | None = None) -> BookingResponse:
        """Mark a booking as manually paid.

        Args:
            booking_id: ID of the booking to mark as paid.
            comment: Optional comment recorded alongside the payment action.

        Returns:
            The updated :class:`~bokamera.models.bookings.BookingResponse`.
        """
        return BookingResponse.from_dict(
            self._http.put(f"/bookings/{booking_id}/markaspaid", {"Comment": comment})
        )

    def refund(self, booking_id: int, payment_log_id: int, *, amount: float) -> dict:
        """Issue a partial or full refund for a payment on a booking.

        Args:
            booking_id: ID of the booking to refund.
            payment_log_id: ID of the payment log entry to refund.
            amount: Amount to refund.

        Returns:
            Raw API response dict for the refund operation.
        """
        return self._http.put(f"/bookings/{booking_id}/refund/{payment_log_id}", {"Amount": amount})

    def move_resources(self, *, resource_id: UUID | str, new_resource_id: UUID | str, test: bool = True) -> BookingResponse:
        """Move all bookings from one resource to another.

        Args:
            resource_id: UUID of the source resource whose bookings should be moved.
            new_resource_id: UUID of the target resource to move the bookings to.
            test: When ``True``, perform a dry-run without saving changes.

        Returns:
            A :class:`~bokamera.models.bookings.BookingResponse` representing the outcome.
        """
        body = {"ResourceId": str(resource_id), "NewResourceId": str(new_resource_id), "Test": test}
        return BookingResponse.from_dict(self._http.put("/bookings/resources/move", body))

    def get_available_resources(self, booking_id: int, resource_type_id: int) -> dict:
        """Retrieve resources of a given type that are available for a booking's time slot.

        Args:
            booking_id: ID of the booking whose time slot is used for availability checking.
            resource_type_id: ID of the resource type to search within.

        Returns:
            Raw API response dict containing the list of available resources.
        """
        return self._http.get(f"/bookings/{booking_id}/resources/available", {"ResourceTypeId": resource_type_id})

    def add_resource(self, booking_id: int, *, resource_type_id: int, resource_id: UUID | str) -> BookingResponse:
        """Add a resource to an existing booking.

        Args:
            booking_id: ID of the booking to modify.
            resource_type_id: ID of the resource type being assigned.
            resource_id: UUID of the specific resource to add.

        Returns:
            The updated :class:`~bokamera.models.bookings.BookingResponse`.
        """
        body = {"ResourceTypeId": resource_type_id, "ResourceId": str(resource_id)}
        return BookingResponse.from_dict(self._http.post(f"/bookings/{booking_id}/resource", body))

    def change_resource(
        self, booking_id: int, *, resource_type_id: int, resource_id: UUID | str, new_resource_id: UUID | str
    ) -> BookingResponse:
        """Swap one resource on a booking for another of the same type.

        Args:
            booking_id: ID of the booking to modify.
            resource_type_id: ID of the resource type both resources belong to.
            resource_id: UUID of the resource currently assigned to the booking.
            new_resource_id: UUID of the resource to assign instead.

        Returns:
            The updated :class:`~bokamera.models.bookings.BookingResponse`.
        """
        body = {
            "ResourceTypeId": resource_type_id,
            "ResourceId": str(resource_id),
            "NewResourceId": str(new_resource_id),
        }
        return BookingResponse.from_dict(self._http.put(f"/bookings/{booking_id}/resource", body))

    def remove_resource(self, booking_id: int, *, resource_type_id: int, resource_id: UUID | str) -> BookingResponse:
        """Remove a resource from an existing booking.

        Args:
            booking_id: ID of the booking to modify.
            resource_type_id: ID of the resource type being removed.
            resource_id: UUID of the specific resource to remove.

        Returns:
            The updated :class:`~bokamera.models.bookings.BookingResponse`.
        """
        params = {"ResourceTypeId": resource_type_id, "ResourceId": str(resource_id)}
        return BookingResponse.from_dict(self._http.delete(f"/bookings/{booking_id}/resource", params))

    def add_quantity(self, booking_id: int, *, quantity: int) -> BookingQuantity:
        """Add a quantity line to a booking.

        Args:
            booking_id: ID of the booking to modify.
            quantity: Number of units to add.

        Returns:
            The newly created :class:`~bokamera.models.bookings.BookingQuantity`.
        """
        return BookingQuantity.from_dict(self._http.post(f"/bookings/{booking_id}/quantity/", {"Quantity": quantity}))

    def update_quantity(self, booking_id: int, quantity_id: int, *, quantity: int, price: float | None = None, vat: float | None = None) -> BookingQuantity:
        """Update a specific quantity line on a booking.

        Args:
            booking_id: ID of the booking to modify.
            quantity_id: ID of the quantity line to update.
            quantity: New quantity value.
            price: Override price for this quantity line.
            vat: Override VAT amount for this quantity line.

        Returns:
            The updated :class:`~bokamera.models.bookings.BookingQuantity`.
        """
        body = {"Quantity": quantity, "Price": price, "VAT": vat}
        return BookingQuantity.from_dict(self._http.put(f"/bookings/{booking_id}/quantity/{quantity_id}", body))

    def update_all_quantities(self, booking_id: int, quantities: list[dict]) -> BookingQuantity:
        """Replace all quantity lines on a booking in a single call.

        Args:
            booking_id: ID of the booking to modify.
            quantities: List of quantity dicts, each containing at minimum ``"Quantity"``.

        Returns:
            The updated :class:`~bokamera.models.bookings.BookingQuantity`.
        """
        return BookingQuantity.from_dict(self._http.put(f"/bookings/{booking_id}/quantity/", {"Quantities": quantities}))

    # ── Reports ─────────────────────────────────────────────────────────────

    def list_reports(self, *, company_id: UUID | str | None = None) -> QueryResponse[ReportResponse]:
        """List available booking report templates.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            A paginated response of :class:`~bokamera.models.bookings.ReportResponse` objects.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return QueryResponse.from_dict(self._http.get("/bookings/reports/", params), ReportResponse)

    def get_report(
        self,
        booking_id: int,
        report_id: int,
        *,
        send_receipt_method: SendReceiptMethod = SendReceiptMethod.PDF_EXPORT,
        company_id: UUID | str | None = None,
    ) -> bytes:
        """Generate and download a report for a specific booking.

        Args:
            booking_id: ID of the booking to generate the report for.
            report_id: ID of the report template to use.
            send_receipt_method: Output format (e.g. PDF export).
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw report bytes (typically a PDF).
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "SendReceiptMethod": int(send_receipt_method),
        }
        return self._http.get_bytes(f"/bookings/{booking_id}/reports/{report_id}", params)

    # ── Booking log ──────────────────────────────────────────────────────────

    def list_log(self, *, company_id: UUID | str, booking_id: int) -> QueryResponse[BookingLogResponse]:
        """List the activity log entries for a booking.

        Args:
            company_id: UUID of the company that owns the booking.
            booking_id: ID of the booking whose log to retrieve.

        Returns:
            A paginated response of :class:`~bokamera.models.bookings.BookingLogResponse` objects.
        """
        params = {"CompanyId": str(company_id), "BookingId": booking_id}
        return QueryResponse.from_dict(self._http.get("/bookinglog", params), BookingLogResponse)

    def add_log(
        self,
        *,
        booking_id: int,
        event_type_id: int,
        created: datetime,
        company_id: UUID | str | None = None,
        comments: str | None = None,
    ) -> BookingLogResponse:
        """Append an activity log entry to a booking.

        Args:
            booking_id: ID of the booking to log against.
            event_type_id: ID of the event type being recorded.
            created: Timestamp for the log entry.
            company_id: Target company (defaults to the client's company).
            comments: Optional free-text comment for the log entry.

        Returns:
            The newly created :class:`~bokamera.models.bookings.BookingLogResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "BookingId": booking_id,
            "EventTypeId": event_type_id,
            "Created": created.isoformat(),
            "Comments": comments,
        }
        return BookingLogResponse.from_dict(self._http.post("/bookinglog", body))

    # ── Booking queue ────────────────────────────────────────────────────────

    def list_queue(
        self,
        *,
        user_id: UUID | str | None = None,
        service_id: int | None = None,
        customer_id: UUID | str | None = None,
        company_id: UUID | str | None = None,
        skip: int | None = None,
        take: int | None = None,
    ) -> list[BookingUserQueueResponse]:
        """List waiting-queue entries.

        Args:
            user_id: Filter by the user who joined the queue.
            service_id: Filter by service ID.
            customer_id: Filter by customer UUID.
            company_id: Target company (defaults to the client's company).
            skip: Pagination offset.
            take: Maximum results to return.

        Returns:
            A list of :class:`~bokamera.models.bookings.BookingUserQueueResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "UserId": str(user_id) if user_id else None,
            "ServiceId": service_id,
            "CustomerId": str(customer_id) if customer_id else None,
            "Skip": skip,
            "Take": take,
        }
        data = self._http.get("/bookinguserqueue/user", params)
        if isinstance(data, list):
            return [BookingUserQueueResponse.from_dict(d) for d in data]
        return [BookingUserQueueResponse.from_dict(d) for d in data.get("Results", [])]

    def get_queue_item(self, queue_id: int, *, company_id: UUID | str | None = None) -> BookingUserQueueResponse:
        """Retrieve a single waiting-queue entry by ID.

        Args:
            queue_id: ID of the queue entry to fetch.
            company_id: Target company (defaults to the client's company).

        Returns:
            The :class:`~bokamera.models.bookings.BookingUserQueueResponse` for this entry.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return BookingUserQueueResponse.from_dict(self._http.get(f"/bookinguserqueue/{queue_id}", params))

    def join_queue(self, *, custom_fields: list[dict] | None = None) -> BookingUserQueueResponse:
        """Add the authenticated user to the waiting queue for a service.

        Args:
            custom_fields: Optional custom field values to submit with the queue entry.

        Returns:
            The newly created :class:`~bokamera.models.bookings.BookingUserQueueResponse`.
        """
        return BookingUserQueueResponse.from_dict(self._http.post("/bookinguserqueue", {"CustomFields": custom_fields or []}))

    def leave_queue(self, queue_id: int, *, company_id: UUID | str | None = None, customer_id: UUID | str | None = None) -> BookingUserQueueResponse:
        """Remove an entry from the waiting queue.

        Args:
            queue_id: ID of the queue entry to remove.
            company_id: Target company (defaults to the client's company).
            customer_id: UUID of the customer leaving the queue, if applicable.

        Returns:
            The removed :class:`~bokamera.models.bookings.BookingUserQueueResponse`.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "CustomerId": str(customer_id) if customer_id else None,
        }
        return BookingUserQueueResponse.from_dict(self._http.delete(f"/bookinguserqueue/{queue_id}", params))

    # ── Printout ─────────────────────────────────────────────────────────────

    def list_printouts(self, *, company_id: UUID | str | None = None) -> QueryResponse[PrintoutResponse]:
        """List available booking printout templates.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            A paginated response of :class:`~bokamera.models.bookings.PrintoutResponse` objects.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return QueryResponse.from_dict(self._http.get("/reports/booking/printout", params), PrintoutResponse)

    def create_printout(self, *, name: str, language: str, **cells: str) -> PrintoutResponse:
        """Create a new booking printout template.

        Args:
            name: Display name for the printout template.
            language: Language/locale code for the template (e.g. ``"sv"``).
            **cells: Additional template cell values passed directly to the API.

        Returns:
            The newly created :class:`~bokamera.models.bookings.PrintoutResponse`.
        """
        body = {"Name": name, "Language": language, **{k: v for k, v in cells.items()}}
        return PrintoutResponse.from_dict(self._http.post("/reports/booking/printout", body))

    def delete_printout(self, printout_id: int, *, company_id: UUID | str | None = None) -> PrintoutResponse:
        """Delete a booking printout template.

        Args:
            printout_id: ID of the printout template to delete.
            company_id: Target company (defaults to the client's company).

        Returns:
            The deleted :class:`~bokamera.models.bookings.PrintoutResponse`.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return PrintoutResponse.from_dict(self._http.delete(f"/reports/booking/printout/{printout_id}", params))

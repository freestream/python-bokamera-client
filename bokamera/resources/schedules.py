"""
Resource namespace for schedule operations.

Exposes methods for creating, listing, updating, and deleting both date-based
and recurring schedules, which control when a service or resource is available
for bookings.
"""

from __future__ import annotations

from datetime import date, time
from uuid import UUID

from .._client import BokaMeraHTTPClient
from ..models.schedules import DateScheduleResponse, RecurringScheduleResponse, ScheduleDate


class ScheduleResource:
    """Schedule operations: CRUD for date schedules and recurring schedules."""

    def __init__(self, http: BokaMeraHTTPClient) -> None:
        self._http = http

    # ── Date schedules ───────────────────────────────────────────────────────

    def list_date(
        self,
        *,
        company_id: UUID | str | None = None,
        valid_from: date | None = None,
        valid_to: date | None = None,
        active: bool | None = None,
        include_schedule_dates: bool | None = None,
        include_connected_resources: bool | None = None,
        include_connected_services: bool | None = None,
    ) -> list[DateScheduleResponse]:
        """List date-based schedules for a company.

        Args:
            company_id: Target company (defaults to the client's company).
            valid_from: Return schedules valid on or after this date.
            valid_to: Return schedules valid on or before this date.
            active: When set, filter by active/inactive status.
            include_schedule_dates: Include individual date entries in each schedule.
            include_connected_resources: Include resources linked to each schedule.
            include_connected_services: Include services linked to each schedule.

        Returns:
            A list of :class:`~bokamera.models.schedules.DateScheduleResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "ValidFrom": valid_from.isoformat() if valid_from else None,
            "ValidTo": valid_to.isoformat() if valid_to else None,
            "Active": active,
            "IncludeScheduleDates": include_schedule_dates,
            "IncludeConnectedResources": include_connected_resources,
            "IncludeConnectedServices": include_connected_services,
        }
        data = self._http.get("/schedules/date", params)
        if isinstance(data, list):
            return [DateScheduleResponse.from_dict(d) for d in data]
        return [DateScheduleResponse.from_dict(d) for d in data.get("Results", [])]

    def create_date(
        self,
        *,
        name: str,
        description: str | None = None,
        active: bool = True,
        number_of_schedule_days: int | None = None,
        schedule_dates: list[ScheduleDate] | None = None,
        resources: list[dict] | None = None,
        services: list[dict] | None = None,
        company_id: UUID | str | None = None,
    ) -> DateScheduleResponse:
        """Create a new date-based schedule.

        Args:
            name: Display name of the schedule.
            description: Optional description of the schedule.
            active: Whether the schedule is immediately active.
            number_of_schedule_days: Number of days the schedule spans.
            schedule_dates: Individual date/time entries for the schedule.
            resources: Resources to link to this schedule.
            services: Services to link to this schedule.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.schedules.DateScheduleResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Name": name,
            "Description": description,
            "Active": active,
            "NumberOfScheduleDays": number_of_schedule_days,
            "ScheduleDates": [s.to_dict() for s in schedule_dates] if schedule_dates else [],
            "Resources": resources or [],
            "Services": services or [],
        }
        return DateScheduleResponse.from_dict(self._http.post("/schedules/date", body))

    def update_date(self, schedule_id: int, *, company_id: UUID | str | None = None, **kwargs: object) -> DateScheduleResponse:
        """Update an existing date-based schedule.

        Args:
            schedule_id: ID of the date schedule to update.
            company_id: Target company (defaults to the client's company).
            **kwargs: Schedule fields to update (e.g. ``Name``, ``Active``).

        Returns:
            The updated :class:`~bokamera.models.schedules.DateScheduleResponse`.
        """
        body = {"CompanyId": str(company_id) if company_id else self._http.default_company_id, **kwargs}
        return DateScheduleResponse.from_dict(self._http.put(f"/schedules/date/{schedule_id}", body))

    def delete_date(self, schedule_id: int, *, company_id: UUID | str | None = None) -> DateScheduleResponse:
        """Delete a date-based schedule.

        Args:
            schedule_id: ID of the date schedule to delete.
            company_id: Target company (defaults to the client's company).

        Returns:
            The deleted :class:`~bokamera.models.schedules.DateScheduleResponse`.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return DateScheduleResponse.from_dict(self._http.delete(f"/schedules/date/{schedule_id}", params))

    # ── Recurring schedules ──────────────────────────────────────────────────

    def create_recurring(
        self,
        *,
        name: str,
        description: str | None = None,
        active: bool = True,
        time_interval: int | None = None,
        valid_from: date | None = None,
        valid_to: date | None = None,
        start_time: time | None = None,
        end_time: time | None = None,
        days_of_week: list[int] | None = None,
        number_of_schedule_days: int | None = None,
        enable_booking_until_closing_time: bool = False,
        schedule_dates: list[ScheduleDate] | None = None,
        exceptions: list[dict] | None = None,
        resources: list[dict] | None = None,
        services: list[dict] | None = None,
        company_id: UUID | str | None = None,
    ) -> RecurringScheduleResponse:
        """Create a new recurring schedule.

        Args:
            name: Display name of the schedule.
            description: Optional description of the schedule.
            active: Whether the schedule is immediately active.
            time_interval: Slot interval in minutes.
            valid_from: Date from which the schedule is active.
            valid_to: Date until which the schedule is active.
            start_time: Daily start time of the availability window.
            end_time: Daily end time of the availability window.
            days_of_week: Days of the week the schedule applies to (0 = Monday).
            number_of_schedule_days: Number of days to include in the schedule.
            enable_booking_until_closing_time: Allow bookings to start at the closing time.
            schedule_dates: Individual override date/time entries.
            exceptions: Date ranges to exclude from the schedule.
            resources: Resources to link to this schedule.
            services: Services to link to this schedule.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.schedules.RecurringScheduleResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Name": name,
            "Description": description,
            "Active": active,
            "TimeInterval": time_interval,
            "ValidFrom": valid_from.isoformat() if valid_from else None,
            "ValidTo": valid_to.isoformat() if valid_to else None,
            "StartTime": start_time.isoformat() if start_time else None,
            "EndTime": end_time.isoformat() if end_time else None,
            "DaysOfWeek": days_of_week or [],
            "NumberOfScheduleDays": number_of_schedule_days,
            "EnableBookingUntilClosingTime": enable_booking_until_closing_time,
            "ScheduleDates": [s.to_dict() for s in schedule_dates] if schedule_dates else [],
            "Exceptions": exceptions or [],
            "Resources": resources or [],
            "Services": services or [],
        }
        return RecurringScheduleResponse.from_dict(self._http.post("/schedules/recurring", body))

    def update_recurring(self, schedule_id: int, *, company_id: UUID | str | None = None, **kwargs: object) -> RecurringScheduleResponse:
        """Update an existing recurring schedule.

        Args:
            schedule_id: ID of the recurring schedule to update.
            company_id: Target company (defaults to the client's company).
            **kwargs: Schedule fields to update (e.g. ``Name``, ``StartTime``, ``DaysOfWeek``).

        Returns:
            The updated :class:`~bokamera.models.schedules.RecurringScheduleResponse`.
        """
        body = {"CompanyId": str(company_id) if company_id else self._http.default_company_id, **kwargs}
        return RecurringScheduleResponse.from_dict(self._http.put(f"/schedules/recurring/{schedule_id}", body))

    def delete_recurring(self, schedule_id: int, *, company_id: UUID | str | None = None) -> RecurringScheduleResponse:
        """Delete a recurring schedule.

        Args:
            schedule_id: ID of the recurring schedule to delete.
            company_id: Target company (defaults to the client's company).

        Returns:
            The deleted :class:`~bokamera.models.schedules.RecurringScheduleResponse`.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return RecurringScheduleResponse.from_dict(self._http.delete(f"/schedules/recurring/{schedule_id}", params))

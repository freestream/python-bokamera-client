"""
Resource namespace for code lock integration operations.

Exposes methods for configuring the general code lock settings and the
provider-specific credentials for all nine supported providers: Accessy,
Amido DAX, Axema, Parakey, RCO Enablea, Siedle, Telkey, Vanderbilt, and Zesec.
Also provides a utility method for cleaning up old reservations.
"""

from __future__ import annotations

from uuid import UUID

from .._client import BokaMeraHTTPClient
from ..models.codelock import (
    CodeLockAccessySettingResponse,
    CodeLockAmidoDaxSettingResponse,
    CodeLockAxemaSettingResponse,
    CodeLockParakeySettingResponse,
    CodeLockRcoEnablaSettingResponse,
    CodeLockSettingResponse,
    CodeLockSiedleSettingResponse,
    CodeLockTelkeySettingResponse,
    CodeLockVanderbiltSettingResponse,
    CodeLockZesecSettingResponse,
)


class CodeLockResource:
    """Code lock integration operations: general settings and all nine provider configurations."""

    def __init__(self, http: BokaMeraHTTPClient) -> None:
        self._http = http

    # ── General ──────────────────────────────────────────────────────────────

    def get_settings(self, *, company_id: UUID | str | None = None, include_options: bool | None = None) -> CodeLockSettingResponse:
        """Retrieve the general code lock integration settings for a company.

        Args:
            company_id: Target company (defaults to the client's company).
            include_options: When ``True``, include available code lock system options.

        Returns:
            A :class:`~bokamera.models.codelock.CodeLockSettingResponse` with the current settings.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "IncludeCodeLockSystemOptions": include_options,
        }
        return CodeLockSettingResponse.from_dict(self._http.get("/codelock/settings", params))

    def update_settings(
        self,
        *,
        active: bool,
        code_lock_systems_id: int,
        valid_before_minutes: int | None = None,
        valid_after_minutes: int | None = None,
        delete_old_by_schedule: bool | None = None,
        send_email_notification: bool | None = None,
        send_sms_notification: bool | None = None,
        email_notification_time: int | None = None,
        sms_notification_time: int | None = None,
        company_id: UUID | str | None = None,
    ) -> CodeLockSettingResponse:
        """Update the general code lock integration settings for a company.

        Args:
            active: Whether the code lock integration should be enabled.
            code_lock_systems_id: ID of the code lock provider system to use.
            valid_before_minutes: Minutes before booking start that the code is valid.
            valid_after_minutes: Minutes after booking end that the code remains valid.
            delete_old_by_schedule: Automatically delete old reservations on a schedule.
            send_email_notification: Send email notification when code is created.
            send_sms_notification: Send SMS notification when code is created.
            email_notification_time: Minutes before booking to send email notification.
            sms_notification_time: Minutes before booking to send SMS notification.
            company_id: Target company (defaults to the client's company).

        Returns:
            The updated :class:`~bokamera.models.codelock.CodeLockSettingResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Active": active,
            "CodeLockSystemsId": code_lock_systems_id,
            **{k: v for k, v in {
                "ValidBeforeMinutes": valid_before_minutes,
                "ValidAfterMinutes": valid_after_minutes,
                "DeleteOldBySchedule": delete_old_by_schedule,
                "SendEmailNotification": send_email_notification,
                "SendSMSNotification": send_sms_notification,
                "EmailNotificationTime": email_notification_time,
                "SMSNotificationTime": sms_notification_time,
            }.items() if v is not None},
        }
        return CodeLockSettingResponse.from_dict(self._http.put("/codelock/settings", body))

    # ── Accessy ──────────────────────────────────────────────────────────────

    def get_accessy(self, *, company_id: UUID | str | None = None) -> CodeLockAccessySettingResponse:
        """Retrieve the Accessy integration credentials for a company.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            A :class:`~bokamera.models.codelock.CodeLockAccessySettingResponse`.
        """
        return CodeLockAccessySettingResponse.from_dict(
            self._http.get("/codelock/accessy/settings", {"CompanyId": str(company_id) if company_id else self._http.default_company_id})
        )

    def create_accessy(self, *, client_id: str, client_secret: str, company_id: UUID | str | None = None) -> CodeLockAccessySettingResponse:
        """Configure Accessy integration credentials for a company.

        Args:
            client_id: OAuth client ID for the Accessy application.
            client_secret: OAuth client secret for the Accessy application.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly configured :class:`~bokamera.models.codelock.CodeLockAccessySettingResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "ClientId": client_id,
            "ClientSecret": client_secret,
        }
        return CodeLockAccessySettingResponse.from_dict(self._http.post("/codelock/accessy/settings", body))

    # ── Amido DAX ────────────────────────────────────────────────────────────

    def get_amido_dax(self, *, company_id: UUID | str | None = None) -> CodeLockAmidoDaxSettingResponse:
        """Retrieve the Amido DAX integration credentials for a company.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            A :class:`~bokamera.models.codelock.CodeLockAmidoDaxSettingResponse`.
        """
        return CodeLockAmidoDaxSettingResponse.from_dict(
            self._http.get("/codelock/amido/dax/settings", {"CompanyId": str(company_id) if company_id else self._http.default_company_id})
        )

    def create_amido_dax(self, *, instance_id: UUID | str, partner_id: UUID | str, company_id: UUID | str | None = None) -> CodeLockAmidoDaxSettingResponse:
        """Configure Amido DAX integration credentials for a company.

        Args:
            instance_id: UUID identifying the company's DAX instance.
            partner_id: UUID of the Amido partner account.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly configured :class:`~bokamera.models.codelock.CodeLockAmidoDaxSettingResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "InstanceId": str(instance_id),
            "PartnerId": str(partner_id),
        }
        return CodeLockAmidoDaxSettingResponse.from_dict(self._http.post("/codelock/amido/dax/settings", body))

    # ── Axema ────────────────────────────────────────────────────────────────

    def get_axema(self, *, company_id: UUID | str | None = None) -> CodeLockAxemaSettingResponse:
        """Retrieve the Axema Vaka integration credentials for a company.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            A :class:`~bokamera.models.codelock.CodeLockAxemaSettingResponse`.
        """
        return CodeLockAxemaSettingResponse.from_dict(
            self._http.get("/codelock/axema/settings", {"CompanyId": str(company_id) if company_id else self._http.default_company_id})
        )

    def create_axema(self, *, api_endpoint: str, api_port: int, username: str, password: str, company_id: UUID | str | None = None) -> CodeLockAxemaSettingResponse:
        """Configure Axema Vaka integration credentials for a company.

        Args:
            api_endpoint: Hostname or IP address of the Axema API server.
            api_port: Port number of the Axema API server.
            username: Account username for authenticating with the Axema API.
            password: Account password for authenticating with the Axema API.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly configured :class:`~bokamera.models.codelock.CodeLockAxemaSettingResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "ApiEndpoint": api_endpoint,
            "ApiPort": api_port,
            "Username": username,
            "Password": password,
        }
        return CodeLockAxemaSettingResponse.from_dict(self._http.post("/codelock/axema/settings", body))

    def update_axema(self, *, company_id: UUID | str | None = None, **kwargs: object) -> CodeLockAxemaSettingResponse:
        """Update existing Axema Vaka integration credentials.

        Args:
            company_id: Target company (defaults to the client's company).
            **kwargs: Credential fields to update (e.g. ``ApiEndpoint``, ``Username``).

        Returns:
            The updated :class:`~bokamera.models.codelock.CodeLockAxemaSettingResponse`.
        """
        body = {"CompanyId": str(company_id) if company_id else self._http.default_company_id, **kwargs}
        return CodeLockAxemaSettingResponse.from_dict(self._http.put("/codelock/axema/settings", body))

    # ── Parakey ──────────────────────────────────────────────────────────────

    def get_parakey(self, *, company_id: UUID | str | None = None) -> CodeLockParakeySettingResponse:
        """Retrieve the Parakey integration credentials for a company.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            A :class:`~bokamera.models.codelock.CodeLockParakeySettingResponse`.
        """
        return CodeLockParakeySettingResponse.from_dict(
            self._http.get("/codelock/parakey/settings", {"CompanyId": str(company_id) if company_id else self._http.default_company_id})
        )

    def create_parakey(self, *, domain_id: str, access_token: str, company_id: UUID | str | None = None) -> CodeLockParakeySettingResponse:
        """Configure Parakey integration credentials for a company.

        Args:
            domain_id: Parakey domain identifier for the company.
            access_token: Bearer token for authenticating with the Parakey API.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly configured :class:`~bokamera.models.codelock.CodeLockParakeySettingResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "DomainId": domain_id,
            "AccessToken": access_token,
        }
        return CodeLockParakeySettingResponse.from_dict(self._http.post("/codelock/parakey/settings", body))

    # ── RCO Enablea ──────────────────────────────────────────────────────────

    def get_rco_enablea(self, *, company_id: UUID | str | None = None) -> CodeLockRcoEnablaSettingResponse:
        """Retrieve the RCO Enablea integration credentials for a company.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            A :class:`~bokamera.models.codelock.CodeLockRcoEnablaSettingResponse`.
        """
        return CodeLockRcoEnablaSettingResponse.from_dict(
            self._http.get("/codelock/rcoenabla/settings", {"CompanyId": str(company_id) if company_id else self._http.default_company_id})
        )

    def create_rco_enablea(self, *, system_id: str, company_id: UUID | str | None = None) -> CodeLockRcoEnablaSettingResponse:
        """Configure RCO Enablea integration credentials for a company.

        Args:
            system_id: Identifier for the RCO system installation.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly configured :class:`~bokamera.models.codelock.CodeLockRcoEnablaSettingResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "SystemId": system_id,
        }
        return CodeLockRcoEnablaSettingResponse.from_dict(self._http.post("/codelock/rcoenabla/settings", body))

    # ── Siedle ───────────────────────────────────────────────────────────────

    def get_siedle(self, *, company_id: UUID | str | None = None) -> CodeLockSiedleSettingResponse:
        """Retrieve the Siedle integration credentials for a company.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            A :class:`~bokamera.models.codelock.CodeLockSiedleSettingResponse`.
        """
        return CodeLockSiedleSettingResponse.from_dict(
            self._http.get("/codelock/siedle/settings", {"CompanyId": str(company_id) if company_id else self._http.default_company_id})
        )

    def create_siedle(self, *, api_endpoint: str, api_port: int, username: str, password: str, integration_type: str, company_id: UUID | str | None = None) -> CodeLockSiedleSettingResponse:
        """Configure Siedle integration credentials for a company.

        Args:
            api_endpoint: Hostname or IP address of the Siedle API server.
            api_port: Port number of the Siedle API server.
            username: Account username for authenticating with the Siedle API.
            password: Account password for authenticating with the Siedle API.
            integration_type: Siedle integration variant (e.g. ``"IP"``, ``"BUS"``).
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly configured :class:`~bokamera.models.codelock.CodeLockSiedleSettingResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "ApiEndpoint": api_endpoint,
            "ApiPort": api_port,
            "Username": username,
            "Password": password,
            "IntegrationType": integration_type,
        }
        return CodeLockSiedleSettingResponse.from_dict(self._http.post("/codelock/siedle/settings", body))

    def update_siedle(self, *, company_id: UUID | str | None = None, **kwargs: object) -> CodeLockSiedleSettingResponse:
        """Update existing Siedle integration credentials.

        Args:
            company_id: Target company (defaults to the client's company).
            **kwargs: Credential fields to update (e.g. ``ApiEndpoint``, ``IntegrationType``).

        Returns:
            The updated :class:`~bokamera.models.codelock.CodeLockSiedleSettingResponse`.
        """
        body = {"CompanyId": str(company_id) if company_id else self._http.default_company_id, **kwargs}
        return CodeLockSiedleSettingResponse.from_dict(self._http.put("/codelock/siedle/settings", body))

    # ── Telkey ───────────────────────────────────────────────────────────────

    def get_telkey(self, *, company_id: UUID | str | None = None) -> CodeLockTelkeySettingResponse:
        """Retrieve the Telkey integration credentials for a company.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            A :class:`~bokamera.models.codelock.CodeLockTelkeySettingResponse`.
        """
        return CodeLockTelkeySettingResponse.from_dict(
            self._http.get("/codelock/telkey/settings", {"CompanyId": str(company_id) if company_id else self._http.default_company_id})
        )

    def create_telkey(self, *, username: str, password: str, company_id: UUID | str | None = None) -> CodeLockTelkeySettingResponse:
        """Configure Telkey integration credentials for a company.

        Args:
            username: Telkey account username.
            password: Telkey account password.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly configured :class:`~bokamera.models.codelock.CodeLockTelkeySettingResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Username": username,
            "Password": password,
        }
        return CodeLockTelkeySettingResponse.from_dict(self._http.post("/codelock/telkey/settings", body))

    # ── Vanderbilt ───────────────────────────────────────────────────────────

    def get_vanderbilt(self, *, company_id: UUID | str | None = None) -> CodeLockVanderbiltSettingResponse:
        """Retrieve the Vanderbilt SPC integration credentials for a company.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            A :class:`~bokamera.models.codelock.CodeLockVanderbiltSettingResponse`.
        """
        return CodeLockVanderbiltSettingResponse.from_dict(
            self._http.get("/codelock/vanderbilt/settings", {"CompanyId": str(company_id) if company_id else self._http.default_company_id})
        )

    def create_vanderbilt(self, *, api_endpoint: str, api_port: int, identifier: str, default_facility_id: str, company_id: UUID | str | None = None) -> CodeLockVanderbiltSettingResponse:
        """Configure Vanderbilt SPC integration credentials for a company.

        Args:
            api_endpoint: Hostname or IP address of the Vanderbilt API gateway.
            api_port: Port number of the Vanderbilt API gateway.
            identifier: API key or site identifier.
            default_facility_id: Default facility/panel ID used when granting access.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly configured :class:`~bokamera.models.codelock.CodeLockVanderbiltSettingResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "ApiEndpoint": api_endpoint,
            "ApiPort": api_port,
            "Identifier": identifier,
            "DefaultFacilityId": default_facility_id,
        }
        return CodeLockVanderbiltSettingResponse.from_dict(self._http.post("/codelock/vanderbilt/settings", body))

    # ── Zesec ────────────────────────────────────────────────────────────────

    def get_zesec(self, *, company_id: UUID | str | None = None) -> CodeLockZesecSettingResponse:
        """Retrieve the Zesec integration credentials for a company.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            A :class:`~bokamera.models.codelock.CodeLockZesecSettingResponse`.
        """
        return CodeLockZesecSettingResponse.from_dict(
            self._http.get("/codelock/zesec/settings", {"CompanyId": str(company_id) if company_id else self._http.default_company_id})
        )

    def create_zesec(self, *, phone_number: str, password: str, company_id: UUID | str | None = None) -> CodeLockZesecSettingResponse:
        """Configure Zesec integration credentials for a company.

        Args:
            phone_number: Phone number registered with the Zesec account.
            password: Zesec account password.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly configured :class:`~bokamera.models.codelock.CodeLockZesecSettingResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "PhoneNumber": phone_number,
            "Password": password,
        }
        return CodeLockZesecSettingResponse.from_dict(self._http.post("/codelock/zesec/settings", body))

    def zesec_unlock(self, *, booking_id: int, company_id: UUID | str | None = None) -> dict:
        """Trigger a Zesec unlock for the door associated with a booking.

        Args:
            booking_id: ID of the booking whose door should be unlocked.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict for the unlock operation.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "BookingId": booking_id,
        }
        return self._http.post("/codelock/zesec/unlock", body)

    # ── Old reservations cleanup ─────────────────────────────────────────────

    def delete_old_reservations(self, code_lock_systems_id: int, *, token: str, to: str | None = None, company_id: UUID | str | None = None) -> dict:
        """Delete old code lock reservations up to a given date.

        Args:
            code_lock_systems_id: ID of the code lock provider system to clean up.
            token: Authentication token authorising the cleanup operation.
            to: ISO datetime string — delete reservations created before this datetime.
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict summarising the deleted reservations.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Token": token,
            "To": to,
        }
        return self._http.post(f"/codelock/{code_lock_systems_id}/reservations/", body)

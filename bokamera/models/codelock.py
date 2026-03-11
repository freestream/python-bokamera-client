"""
Data models for the code lock integrations resource.

Contains dataclasses for the general code lock settings as well as
provider-specific configuration models for all nine supported code lock
providers: Accessy, Amido DAX, Axema, Parakey, RCO Enablea, Siedle, Telkey,
Vanderbilt, and Zesec.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from .common import _dt, _uuid


@dataclass(slots=True)
class CodeLockSettingResponse:
    """General code lock integration settings for a company.

    Attributes:
        company_id: UUID of the company.
        active: Whether the code lock integration is currently enabled.
        code_lock_systems_id: ID of the selected code lock provider system.
        code_lock_system_name: Display name of the selected provider.
    """

    company_id: UUID | None = None
    active: bool = False
    code_lock_systems_id: int | None = None
    code_lock_system_name: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CodeLockSettingResponse:
        """Construct a CodeLockSettingResponse from a raw API response dict."""
        return cls(
            company_id=_uuid(d.get("CompanyId")),
            active=d.get("Active", False),
            code_lock_systems_id=d.get("CodeLockSystemsId"),
            code_lock_system_name=d.get("CodeLockSystemName"),
        )


@dataclass(slots=True)
class CodeLockAccessySettingResponse:
    """Accessy code lock integration credentials.

    Attributes:
        client_id: OAuth client ID for the Accessy application.
        client_secret: OAuth client secret for the Accessy application.
        created: Timestamp when the integration was configured.
        updated: Timestamp of the most recent configuration update.
    """

    client_id: str | None = None
    client_secret: str | None = None
    created: datetime | None = None
    updated: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CodeLockAccessySettingResponse:
        """Construct a CodeLockAccessySettingResponse from a raw API response dict."""
        return cls(
            client_id=d.get("ClientId"),
            client_secret=d.get("ClientSecret"),
            created=_dt(d.get("Created")),
            updated=_dt(d.get("Updated")),
        )


@dataclass(slots=True)
class CodeLockAmidoDaxSettingResponse:
    """Amido DAX code lock integration credentials.

    Attributes:
        instance_id: UUID identifying the company's DAX instance.
        partner_id: UUID of the Amido partner account.
        created: Timestamp when the integration was configured.
        updated: Timestamp of the most recent configuration update.
    """

    instance_id: str | None = None
    partner_id: str | None = None
    created: datetime | None = None
    updated: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CodeLockAmidoDaxSettingResponse:
        """Construct a CodeLockAmidoDaxSettingResponse from a raw API response dict."""
        return cls(
            instance_id=d.get("InstanceId"),
            partner_id=d.get("PartnerId"),
            created=_dt(d.get("Created")),
            updated=_dt(d.get("Updated")),
        )


@dataclass(slots=True)
class CodeLockAxemaSettingResponse:
    """Axema Vaka code lock integration credentials.

    Attributes:
        api_endpoint: Hostname or IP address of the Axema API server.
        api_port: Port number of the Axema API server.
        username: Account username for authenticating with the Axema API.
        created: Timestamp when the integration was configured.
        updated: Timestamp of the most recent configuration update.
    """

    api_endpoint: str | None = None
    api_port: int | None = None
    username: str | None = None
    created: datetime | None = None
    updated: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CodeLockAxemaSettingResponse:
        """Construct a CodeLockAxemaSettingResponse from a raw API response dict."""
        return cls(
            api_endpoint=d.get("ApiEndpoint"),
            api_port=d.get("ApiPort"),
            username=d.get("Username"),
            created=_dt(d.get("Created")),
            updated=_dt(d.get("Updated")),
        )


@dataclass(slots=True)
class CodeLockParakeySettingResponse:
    """Parakey code lock integration credentials.

    Attributes:
        domain_id: Parakey domain identifier for the company.
        access_token: Bearer token for authenticating with the Parakey API.
        created: Timestamp when the integration was configured.
        updated: Timestamp of the most recent configuration update.
    """

    domain_id: str | None = None
    access_token: str | None = None
    created: datetime | None = None
    updated: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CodeLockParakeySettingResponse:
        """Construct a CodeLockParakeySettingResponse from a raw API response dict."""
        return cls(
            domain_id=d.get("DomainId"),
            access_token=d.get("AccessToken"),
            created=_dt(d.get("Created")),
            updated=_dt(d.get("Updated")),
        )


@dataclass(slots=True)
class CodeLockRcoEnablaSettingResponse:
    """RCO Enablea code lock integration credentials.

    Attributes:
        system_id: Identifier for the RCO system installation.
        client_id: Client identifier for API authentication.
        created: Timestamp when the integration was configured.
        updated: Timestamp of the most recent configuration update.
    """

    system_id: str | None = None
    client_id: str | None = None
    created: datetime | None = None
    updated: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CodeLockRcoEnablaSettingResponse:
        """Construct a CodeLockRcoEnablaSettingResponse from a raw API response dict."""
        return cls(
            system_id=d.get("SystemId"),
            client_id=d.get("ClientId"),
            created=_dt(d.get("Created")),
            updated=_dt(d.get("Updated")),
        )


@dataclass(slots=True)
class CodeLockSiedleSettingResponse:
    """Siedle code lock integration credentials.

    Attributes:
        api_endpoint: Hostname or IP address of the Siedle API server.
        api_port: Port number of the Siedle API server.
        username: Account username for authenticating with the Siedle API.
        integration_type: Siedle integration variant (e.g. ``"IP"``, ``"BUS"``).
        device_id: Identifier of the specific Siedle device.
        created: Timestamp when the integration was configured.
        updated: Timestamp of the most recent configuration update.
    """

    api_endpoint: str | None = None
    api_port: int | None = None
    username: str | None = None
    integration_type: str | None = None
    device_id: str | None = None
    created: datetime | None = None
    updated: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CodeLockSiedleSettingResponse:
        """Construct a CodeLockSiedleSettingResponse from a raw API response dict."""
        return cls(
            api_endpoint=d.get("ApiEndpoint"),
            api_port=d.get("ApiPort"),
            username=d.get("Username"),
            integration_type=d.get("IntegrationType"),
            device_id=d.get("DeviceId"),
            created=_dt(d.get("Created")),
            updated=_dt(d.get("Updated")),
        )


@dataclass(slots=True)
class CodeLockTelkeySettingResponse:
    """Telkey code lock integration credentials.

    Attributes:
        username: Telkey account username.
        created: Timestamp when the integration was configured.
        updated: Timestamp of the most recent configuration update.
    """

    username: str | None = None
    created: datetime | None = None
    updated: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CodeLockTelkeySettingResponse:
        """Construct a CodeLockTelkeySettingResponse from a raw API response dict."""
        return cls(
            username=d.get("Username"),
            created=_dt(d.get("Created")),
            updated=_dt(d.get("Updated")),
        )


@dataclass(slots=True)
class CodeLockVanderbiltSettingResponse:
    """Vanderbilt SPC code lock integration credentials.

    Attributes:
        api_endpoint: Hostname or IP address of the Vanderbilt API gateway.
        api_port: Port number of the Vanderbilt API gateway.
        identifier: API key or site identifier.
        default_facility_id: Default facility/panel ID used when granting access.
        created: Timestamp when the integration was configured.
        updated: Timestamp of the most recent configuration update.
    """

    api_endpoint: str | None = None
    api_port: int | None = None
    identifier: str | None = None
    default_facility_id: str | None = None
    created: datetime | None = None
    updated: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CodeLockVanderbiltSettingResponse:
        """Construct a CodeLockVanderbiltSettingResponse from a raw API response dict."""
        return cls(
            api_endpoint=d.get("ApiEndpoint"),
            api_port=d.get("ApiPort"),
            identifier=d.get("Identifier"),
            default_facility_id=d.get("DefaultFacilityId"),
            created=_dt(d.get("Created")),
            updated=_dt(d.get("Updated")),
        )


@dataclass(slots=True)
class CodeLockZesecSettingResponse:
    """Zesec code lock integration credentials.

    Attributes:
        phone_number: Phone number registered with the Zesec account.
        created: Timestamp when the integration was configured.
        updated: Timestamp of the most recent configuration update.
    """

    phone_number: str | None = None
    created: datetime | None = None
    updated: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CodeLockZesecSettingResponse:
        """Construct a CodeLockZesecSettingResponse from a raw API response dict."""
        return cls(
            phone_number=d.get("PhoneNumber"),
            created=_dt(d.get("Created")),
            updated=_dt(d.get("Updated")),
        )

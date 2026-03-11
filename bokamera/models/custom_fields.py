"""
Data models for the custom fields resource.

Contains dataclasses for custom field definitions, storage slot availability,
and validation rule lookups.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID

from .common import _uuid


@dataclass(slots=True)
class CustomFieldValidationResponse:
    """A regex-based validation rule for custom field values.

    Attributes:
        id: Validation rule ID.
        name: Human-readable name of the validation rule.
        reg_ex_code: Regular expression pattern used to validate input.
    """

    id: int | None = None
    name: str | None = None
    reg_ex_code: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> CustomFieldValidationResponse:
        """Construct a CustomFieldValidationResponse from a raw API response dict."""
        return cls(id=d.get("Id"), name=d.get("Name"), reg_ex_code=d.get("RegExCode"))


@dataclass(slots=True)
class CustomFieldResponse:
    """A custom field definition that captures additional data during booking.

    Attributes:
        id: Custom field ID.
        name: Label displayed to the user.
        description: Helper text displayed beneath the field.
        datatype: Data type of the field (e.g. ``"TextInput"``, ``"Checkbox"``).
        default_value: Pre-filled value shown to the user.
        is_mandatory: Whether the field must be filled in before booking.
        max_length: Maximum allowed character length for text fields.
        is_public: Whether the field is visible to customers (as opposed to admins only).
        is_hidden: Whether the field is hidden from the booking form entirely.
        sort_order: Display order relative to other custom fields.
        active: Whether this custom field is currently active.
        mandatory_error_message: Error message shown when a mandatory field is left empty.
        values: Predefined selectable values (for dropdown / checkbox fields).
        services: Services this custom field is connected to.
    """

    id: int | None = None
    name: str | None = None
    description: str | None = None
    datatype: str | None = None
    default_value: str | None = None
    is_mandatory: bool = False
    max_length: int | None = None
    is_public: bool = True
    is_hidden: bool = False
    sort_order: int | None = None
    active: bool = True
    mandatory_error_message: str | None = None
    values: list[dict] = field(default_factory=list)
    services: list[dict] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> CustomFieldResponse:
        """Construct a CustomFieldResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            name=d.get("Name"),
            description=d.get("Description"),
            datatype=d.get("Datatype"),
            default_value=d.get("DefaultValue"),
            is_mandatory=d.get("IsMandatory", False),
            max_length=d.get("MaxLength"),
            is_public=d.get("IsPublic", True),
            is_hidden=d.get("IsHidden", False),
            sort_order=d.get("SortOrder"),
            active=d.get("Active", True),
            mandatory_error_message=d.get("MandatoryErrorMessage"),
            values=d.get("Values", []),
            services=d.get("Services", []),
        )


@dataclass(slots=True)
class CustomFieldSlotResponse:
    """A storage slot in the database for a custom field value.

    BokaMera stores custom field values in a fixed number of typed columns.
    This model represents one such column's metadata and occupancy.

    Attributes:
        table: Name of the database table that holds this slot.
        id: Slot number within the table.
        name: Human-readable name currently assigned to this slot.
        datatype: Data type of values stored in this slot.
        occupied: Whether this slot is already used by an existing custom field.
    """

    table: str | None = None
    id: int | None = None
    name: str | None = None
    datatype: str | None = None
    occupied: bool = False

    @classmethod
    def from_dict(cls, d: dict) -> CustomFieldSlotResponse:
        """Construct a CustomFieldSlotResponse from a raw API response dict."""
        return cls(
            table=d.get("Table"),
            id=d.get("Id"),
            name=d.get("Name"),
            datatype=d.get("Datatype"),
            occupied=d.get("Occupied", False),
        )

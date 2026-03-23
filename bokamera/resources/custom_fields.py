"""
Resource namespace for custom field operations.

Exposes methods for creating, listing, updating, and deleting custom fields,
as well as listing the available slot definitions and validation rule patterns.
"""

from __future__ import annotations

from uuid import UUID

from .._client import BokaMeraHTTPClient
from ..models.common import QueryResponse
from ..models.custom_fields import CustomFieldResponse, CustomFieldSlotResponse, CustomFieldValidationResponse


class CustomFieldResource:
    """Custom field operations: CRUD, slot listing, and validation rules."""

    def __init__(self, http: BokaMeraHTTPClient) -> None:
        self._http = http

    def list(
        self,
        *,
        table: str,
        company_id: UUID | str | None = None,
        ids: list[int] | None = None,
        active: bool | None = None,
        include_custom_field_values: bool | None = None,
        include_connected_services: bool | None = None,
    ) -> list[CustomFieldResponse]:
        """List custom fields for a company.

        Args:
            table: The entity table the custom fields belong to (e.g. ``"Booking"``).
            company_id: Target company (defaults to the client's company).
            ids: Filter to custom fields with these IDs.
            active: When set, filter by active/inactive status.
            include_custom_field_values: Include the allowed value options for each field.
            include_connected_services: Include services the field is attached to.

        Returns:
            A list of :class:`~bokamera.models.custom_fields.CustomFieldResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Table": table,
            "Ids": ids,
            "Active": active,
            "IncludeCustomFieldValues": include_custom_field_values,
            "IncludeConnectedServices": include_connected_services,
        }
        data = self._http.get("/customfields", params)
        if isinstance(data, list):
            return [CustomFieldResponse.from_dict(d) for d in data]
        return [CustomFieldResponse.from_dict(d) for d in data.get("Results", [])]

    def create(
        self,
        *,
        name: str,
        datatype: str,
        description: str | None = None,
        icon_id: int | None = None,
        default_value: str | None = None,
        is_mandatory: bool = False,
        max_length: int | None = None,
        reg_ex_id: int | None = None,
        is_public: bool = True,
        is_hidden: bool = False,
        sort_order: int | None = None,
        values: list[dict] | None = None,
        services: list[dict] | None = None,
        field_id: int | None = None,
        width: int | None = None,
        mandatory_error_message: str | None = None,
        multiple_line_text: bool | None = None,
        reg_ex_error_message: str | None = None,
        company_id: UUID | str | None = None,
    ) -> CustomFieldResponse:
        """Create a new custom field.

        Args:
            name: Display label for the custom field.
            datatype: Data type of the field (e.g. ``"TextBox"``, ``"SelectList"``).
            description: Optional help text shown to the user.
            icon_id: ID of the icon to display alongside the field.
            default_value: Default value pre-filled in the field.
            is_mandatory: Whether the field must be filled before submitting.
            max_length: Maximum character length for text fields.
            reg_ex_id: ID of a validation regex pattern to apply.
            is_public: Whether the field is visible to customers.
            is_hidden: Whether the field is hidden from view.
            sort_order: Position of the field relative to other custom fields.
            values: Allowed value options (for select-type fields).
            services: Services this custom field is attached to.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.custom_fields.CustomFieldResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "FieldId": field_id,
            "Name": name,
            "Description": description,
            "IconId": icon_id,
            "Width": width,
            "Datatype": datatype,
            "DefaultValue": default_value,
            "IsMandatory": is_mandatory,
            "MandatoryErrorMessage": mandatory_error_message,
            "MaxLength": max_length,
            "MultipleLineText": multiple_line_text,
            "RegExId": reg_ex_id,
            "RegExErrorMessage": reg_ex_error_message,
            "IsPublic": is_public,
            "IsHidden": is_hidden,
            "SortOrder": sort_order,
            "Values": values or [],
            "Services": services or [],
        }
        return CustomFieldResponse.from_dict(self._http.post("/customfields", body))

    def update(self, field_id: int, *, company_id: UUID | str | None = None, **kwargs: object) -> CustomFieldResponse:
        """Update an existing custom field.

        Args:
            field_id: ID of the custom field to update.
            company_id: Target company (defaults to the client's company).
            **kwargs: Custom field attributes to update (e.g. ``Name``, ``IsMandatory``).

        Returns:
            The updated :class:`~bokamera.models.custom_fields.CustomFieldResponse`.
        """
        body = {"CompanyId": str(company_id) if company_id else self._http.default_company_id, **kwargs}
        return CustomFieldResponse.from_dict(self._http.put(f"/customfields/{field_id}", body))

    def delete(self, *, company_id: UUID | str | None = None) -> dict:
        """Delete all custom fields for a company.

        Args:
            company_id: Target company (defaults to the client's company).

        Returns:
            Raw API response dict for the deletion.
        """
        return self._http.delete("/customfields", {"CompanyId": str(company_id) if company_id else self._http.default_company_id})

    def list_slots(
        self,
        *,
        table: str,
        company_id: UUID | str | None = None,
        free_slots: bool | None = None,
    ) -> list[CustomFieldSlotResponse]:
        """List custom field slot definitions for an entity table.

        Args:
            table: The entity table to query (e.g. ``"Booking"``).
            company_id: Target company (defaults to the client's company).
            free_slots: When ``True``, return only unoccupied slots.

        Returns:
            A list of :class:`~bokamera.models.custom_fields.CustomFieldSlotResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Table": table,
            "FreeSlots": free_slots,
        }
        data = self._http.get("/customfields/slots", params)
        if isinstance(data, list):
            return [CustomFieldSlotResponse.from_dict(d) for d in data]
        return [CustomFieldSlotResponse.from_dict(d) for d in data.get("Results", [])]

    def list_validations(
        self,
        *,
        id_: int | None = None,
        name: str | None = None,
        reg_ex_code: str | None = None,
    ) -> list[CustomFieldValidationResponse]:
        """List available custom field validation rules.

        Args:
            id_: Filter to a single validation rule by ID.
            name: Filter by rule name.
            reg_ex_code: Filter by regex pattern code.

        Returns:
            A list of :class:`~bokamera.models.custom_fields.CustomFieldValidationResponse` objects.
        """
        params = {"Id": id_, "Name": name, "RegExCode": reg_ex_code}
        data = self._http.get("/customfields/validations", params)
        if isinstance(data, list):
            return [CustomFieldValidationResponse.from_dict(d) for d in data]
        return [CustomFieldValidationResponse.from_dict(d) for d in data.get("Results", [])]

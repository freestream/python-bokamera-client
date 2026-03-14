"""
Resource namespace for support case operations.

Exposes methods for creating, listing, and updating support cases, as well as
adding comments and attachments to cases, and listing case status options.
"""

from __future__ import annotations

from uuid import UUID

from .._client import BokaMeraHTTPClient
from ..models.common import QueryResponse
from ..models.support import (
    SupportCaseAttachmentResponse,
    SupportCaseCommentResponse,
    SupportCaseResponse,
    SupportCaseStatusResponse,
)


class SupportResource:
    """Support case operations: CRUD, comments, attachments, and statuses."""

    def __init__(self, http: BokaMeraHTTPClient) -> None:
        self._http = http

    def list(
        self,
        *,
        company_id: UUID | str | None = None,
        active: bool | None = None,
        id_: int | None = None,
        include_comments: bool | None = None,
        include_case_status_information: bool | None = None,
        include_case_type_information: bool | None = None,
        include_case_area_information: bool | None = None,
        include_case_attachments: bool | None = None,
        include_case_status_options: bool | None = None,
        include_case_type_options: bool | None = None,
        include_case_area_options: bool | None = None,
    ) -> list[SupportCaseResponse]:
        """List support cases for a company.

        Args:
            company_id: Target company (defaults to the client's company).
            active: When set, filter by active/inactive status.
            id_: Filter to a single case by ID.
            include_comments: Include comments in each case.
            include_case_status_information: Include status label details.
            include_case_type_information: Include case type details.
            include_case_area_information: Include case area details.
            include_case_attachments: Include file attachments in each case.
            include_case_status_options: Include available status options for UI dropdowns.
            include_case_type_options: Include available case type options for UI dropdowns.
            include_case_area_options: Include available case area options for UI dropdowns.

        Returns:
            A list of :class:`~bokamera.models.support.SupportCaseResponse` objects.
        """
        params = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Active": active,
            "Id": id_,
            "IncludeComments": include_comments,
            "IncludeCaseStatusInformation": include_case_status_information,
            "IncludeCaseTypeInformation": include_case_type_information,
            "IncludeCaseAreaInformation": include_case_area_information,
            "IncludeCaseAttachments": include_case_attachments,
            "IncludeCaseStatusOptions": include_case_status_options,
            "IncludeCaseTypeOptions": include_case_type_options,
            "IncludeCaseAreaOptions": include_case_area_options,
        }
        data = self._http.get("/support/cases", params)
        if isinstance(data, list):
            return [SupportCaseResponse.from_dict(d) for d in data]
        return [SupportCaseResponse.from_dict(d) for d in data.get("Results", [])]

    def create(
        self,
        *,
        title: str,
        description: str,
        case_type_id: int | None = None,
        case_area_id: int | None = None,
        company_id: UUID | str | None = None,
    ) -> SupportCaseResponse:
        """Create a new support case.

        Args:
            title: Brief summary of the issue.
            description: Detailed description of the issue.
            case_type_id: ID of the support case type category.
            case_area_id: ID of the support area this case belongs to.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.support.SupportCaseResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Title": title,
            "Description": description,
            "CaseTypeId": case_type_id,
            "CaseAreaId": case_area_id,
        }
        return SupportCaseResponse.from_dict(self._http.post("/support/cases", body))

    def update(self, case_id: int, *, company_id: UUID | str | None = None, **kwargs: object) -> SupportCaseResponse:
        """Update an existing support case.

        Args:
            case_id: ID of the support case to update.
            company_id: Target company (defaults to the client's company).
            **kwargs: Case fields to update (e.g. ``Title``, ``StatusId``).

        Returns:
            The updated :class:`~bokamera.models.support.SupportCaseResponse`.
        """
        body = {"CompanyId": str(company_id) if company_id else self._http.default_company_id, **kwargs}
        return SupportCaseResponse.from_dict(self._http.put(f"/support/cases/{case_id}", body))

    def add_comment(self, case_id: int, *, comment: str, company_id: UUID | str | None = None) -> SupportCaseCommentResponse:
        """Add a comment to a support case.

        Args:
            case_id: ID of the support case to comment on.
            comment: Comment text to add.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.support.SupportCaseCommentResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "Comment": comment,
        }
        return SupportCaseCommentResponse.from_dict(self._http.post(f"/support/cases/{case_id}/comments", body))

    def delete_comment(self, case_id: int, comment_id: int, *, company_id: UUID | str | None = None) -> SupportCaseCommentResponse:
        """Delete a comment from a support case.

        Args:
            case_id: ID of the support case.
            comment_id: ID of the comment to delete.
            company_id: Target company (defaults to the client's company).

        Returns:
            The deleted :class:`~bokamera.models.support.SupportCaseCommentResponse`.
        """
        params = {"CompanyId": str(company_id) if company_id else self._http.default_company_id}
        return SupportCaseCommentResponse.from_dict(self._http.delete(f"/support/cases/{case_id}/comments/{comment_id}", params))

    def add_attachment(self, case_id: int, *, file_url: str, company_id: UUID | str | None = None) -> SupportCaseAttachmentResponse:
        """Attach a file to a support case.

        Args:
            case_id: ID of the support case to attach the file to.
            file_url: URL of the file to attach.
            company_id: Target company (defaults to the client's company).

        Returns:
            The newly created :class:`~bokamera.models.support.SupportCaseAttachmentResponse`.
        """
        body = {
            "CompanyId": str(company_id) if company_id else self._http.default_company_id,
            "FileUrl": file_url,
        }
        return SupportCaseAttachmentResponse.from_dict(self._http.post(f"/support/cases/{case_id}/attachments", body))

    def list_statuses(self, *, skip: int | None = None, take: int | None = None) -> QueryResponse[SupportCaseStatusResponse]:
        """List available support case status options.

        Args:
            skip: Pagination offset.
            take: Maximum results to return.

        Returns:
            A paginated response of :class:`~bokamera.models.support.SupportCaseStatusResponse` objects.
        """
        return QueryResponse.from_dict(
            self._http.get("/support/cases/status", {"Skip": skip, "Take": take}),
            SupportCaseStatusResponse,
        )

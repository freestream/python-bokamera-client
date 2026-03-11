"""
Data models for the support resource.

Contains dataclasses for support case status options, case records,
comments, and file attachments.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from .common import _dt, _uuid


@dataclass(slots=True)
class SupportCaseStatusResponse:
    """A support case status option (e.g. Open, In Progress, Resolved).

    Attributes:
        id: Status ID.
        name: Short status name.
        description: Longer description of what the status means.
        icon: Icon identifier used in the admin UI.
        color: Hex colour code associated with the status.
    """

    id: int | None = None
    name: str | None = None
    description: str | None = None
    icon: str | None = None
    color: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> SupportCaseStatusResponse:
        """Construct a SupportCaseStatusResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            name=d.get("Name"),
            description=d.get("Description"),
            icon=d.get("Icon"),
            color=d.get("Color"),
        )


@dataclass(slots=True)
class SupportCaseCommentResponse:
    """A comment added to a support case by a user or support agent.

    Attributes:
        id: Comment ID.
        comment: The comment text body.
        created_by: Name or identifier of the person who posted the comment.
        created: Timestamp when the comment was posted.
    """

    id: int | None = None
    comment: str | None = None
    created_by: str | None = None
    created: datetime | None = None

    @classmethod
    def from_dict(cls, d: dict) -> SupportCaseCommentResponse:
        """Construct a SupportCaseCommentResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            comment=d.get("Comment"),
            created_by=d.get("CreatedBy"),
            created=_dt(d.get("Created")),
        )


@dataclass(slots=True)
class SupportCaseAttachmentResponse:
    """A file attachment uploaded to a support case.

    Attributes:
        id: Attachment record ID.
        file_url: Public URL at which the file can be downloaded.
    """

    id: int | None = None
    file_url: str | None = None

    @classmethod
    def from_dict(cls, d: dict) -> SupportCaseAttachmentResponse:
        """Construct a SupportCaseAttachmentResponse from a raw API response dict."""
        return cls(id=d.get("Id"), file_url=d.get("FileUrl"))


@dataclass(slots=True)
class SupportCaseResponse:
    """A support case submitted by a company to BokaMera support.

    Attributes:
        id: Case ID.
        company_id: UUID of the company that submitted the case.
        title: Short summary of the issue.
        description: Full description of the issue.
        case_type_id: ID of the case type category.
        case_area_id: ID of the functional area the issue relates to.
        active: Whether the case is still open.
        created: Timestamp when the case was submitted.
        updated: Timestamp of the most recent modification.
        comments: Conversation thread for this case.
        attachments: Files attached to this case.
    """

    id: int | None = None
    company_id: UUID | None = None
    title: str | None = None
    description: str | None = None
    case_type_id: int | None = None
    case_area_id: int | None = None
    active: bool = True
    created: datetime | None = None
    updated: datetime | None = None
    comments: list[SupportCaseCommentResponse] = field(default_factory=list)
    attachments: list[SupportCaseAttachmentResponse] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict) -> SupportCaseResponse:
        """Construct a SupportCaseResponse from a raw API response dict."""
        return cls(
            id=d.get("Id"),
            company_id=_uuid(d.get("CompanyId")),
            title=d.get("Title"),
            description=d.get("Description"),
            case_type_id=d.get("CaseTypeId"),
            case_area_id=d.get("CaseAreaId"),
            active=d.get("Active", True),
            created=_dt(d.get("Created")),
            updated=_dt(d.get("Updated")),
            comments=[SupportCaseCommentResponse.from_dict(c) for c in d.get("Comments", [])],
            attachments=[SupportCaseAttachmentResponse.from_dict(a) for a in d.get("Attachments", [])],
        )

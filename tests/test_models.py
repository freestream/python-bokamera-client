"""Tests for model from_dict() classmethods."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

import pytest

from bokamera.models.articles import ArticleResponse, ArticleTypeResponse
from bokamera.models.billing import BillingMethodResponse, CompanyInvoiceResponse
from bokamera.models.bookings import BookingCustomer, BookingQuantity, BookingResponse
from bokamera.models.common import (
    CountryResponse,
    CurrencyResponse,
    CustomFieldValue,
    InvoiceAddress,
    QueryResponse,
)
from bokamera.models.companies import CompanyResponse, CompanyTypeResponse
from bokamera.models.customers import CustomerArticleResponse, CustomerResponse
from bokamera.models.licenses import CompanyLicenseResponse, CompanyTrialResponse
from bokamera.models.rebate_codes import (
    RebateCodeResponse,
    RebateCodeStatusResponse,
    RebateCodeTypeResponse,
)
from bokamera.models.resources import ResourceResponse, ResourceTypeResponse
from bokamera.models.services import DurationTypeResponse, ServicePriceResponse, ServiceResponse
from bokamera.models.support import SupportCaseResponse, SupportCaseStatusResponse
from bokamera.models.custom_fields import CustomFieldResponse, CustomFieldValidationResponse
from bokamera.models.homepage import HomepageImageResponse, HomepageSettingsResponse


COMPANY_UUID_STR = "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
COMPANY_UUID = UUID(COMPANY_UUID_STR)
CUSTOMER_UUID_STR = "11111111-2222-3333-4444-555555555555"
CUSTOMER_UUID = UUID(CUSTOMER_UUID_STR)


# ---------------------------------------------------------------------------
# ServiceResponse
# ---------------------------------------------------------------------------


class TestServiceResponse:
    def test_from_dict_full(self):
        d = {
            "Id": 42,
            "Name": "Yoga Class",
            "Description": "A relaxing session",
            "Group": "Fitness",
            "Active": True,
            "BookingStatusId": 1,
            "Duration": 60,
            "DurationTypeId": 2,
            "TotalSpots": 10,
            "ImageUrl": "https://example.com/yoga.png",
            "IsPaymentEnabled": True,
            "EnableBookingQueue": False,
        }
        svc = ServiceResponse.from_dict(d)
        assert svc.id == 42
        assert svc.name == "Yoga Class"
        assert svc.description == "A relaxing session"
        assert svc.group == "Fitness"
        assert svc.active is True
        assert svc.booking_status_id == 1
        assert svc.duration == 60
        assert svc.duration_type_id == 2
        assert svc.total_spots == 10
        assert svc.image_url == "https://example.com/yoga.png"
        assert svc.is_payment_enabled is True
        assert svc.enable_booking_queue is False

    def test_from_dict_defaults_when_empty(self):
        svc = ServiceResponse.from_dict({})
        assert svc.id is None
        assert svc.name is None
        assert svc.active is True
        assert svc.is_payment_enabled is False
        assert svc.enable_booking_queue is False
        assert svc.prices == []
        assert svc.custom_fields == []

    def test_from_dict_parses_nested_prices(self):
        d = {
            "Id": 1,
            "Name": "Massage",
            "Prices": [{"Id": 10, "Price": 500.0, "CurrencyId": "SEK"}],
        }
        svc = ServiceResponse.from_dict(d)
        assert len(svc.prices) == 1
        assert svc.prices[0].id == 10
        assert svc.prices[0].price == 500.0

    def test_duration_type_response(self):
        d = {"Id": 1, "Name": "Fixed"}
        dt = DurationTypeResponse.from_dict(d)
        assert dt.id == 1
        assert dt.name == "Fixed"

    def test_duration_type_response_empty(self):
        dt = DurationTypeResponse.from_dict({})
        assert dt.id is None
        assert dt.name is None


# ---------------------------------------------------------------------------
# BookingResponse
# ---------------------------------------------------------------------------


class TestBookingResponse:
    def test_from_dict_full(self):
        d = {
            "Id": 100,
            "CompanyId": COMPANY_UUID_STR,
            "From": "2026-01-15T10:00:00Z",
            "To": "2026-01-15T11:00:00Z",
            "StatusId": 1,
            "Status": "Confirmed",
            "ServiceId": 5,
            "ServiceName": "Haircut",
            "TotalPrice": 250.0,
            "CancellationCode": "ABC123",
        }
        b = BookingResponse.from_dict(d)
        assert b.id == 100
        assert b.company_id == COMPANY_UUID
        assert isinstance(b.company_id, UUID)
        assert b.from_ == datetime(2026, 1, 15, 10, 0, 0, tzinfo=timezone.utc)
        assert b.to == datetime(2026, 1, 15, 11, 0, 0, tzinfo=timezone.utc)
        assert b.status_id == 1
        assert b.status == "Confirmed"
        assert b.service_id == 5
        assert b.service_name == "Haircut"
        assert b.total_price == 250.0
        assert b.cancellation_code == "ABC123"

    def test_from_dict_parses_customer(self):
        d = {
            "Id": 1,
            "Customer": {
                "Firstname": "Anna",
                "Lastname": "Svensson",
                "Email": "anna@example.com",
                "Phone": "+46701234567",
                "CustomerId": CUSTOMER_UUID_STR,
            },
        }
        b = BookingResponse.from_dict(d)
        assert b.customer is not None
        assert b.customer.firstname == "Anna"
        assert b.customer.email == "anna@example.com"
        assert b.customer.customer_id == CUSTOMER_UUID

    def test_from_dict_defaults_when_empty(self):
        b = BookingResponse.from_dict({})
        assert b.id is None
        assert b.from_ is None
        assert b.to is None
        assert b.customer is None
        assert b.quantities == []
        assert b.resources == []

    def test_from_dict_parses_quantities(self):
        d = {
            "Id": 1,
            "Quantities": [{"Id": 1, "Quantity": 2, "Price": 100.0, "VAT": 25.0}],
        }
        b = BookingResponse.from_dict(d)
        assert len(b.quantities) == 1
        assert b.quantities[0].quantity == 2
        assert b.quantities[0].price == 100.0


# ---------------------------------------------------------------------------
# QueryResponse
# ---------------------------------------------------------------------------


class TestQueryResponse:
    def test_from_dict_with_results(self):
        data = {
            "Results": [
                {"Id": 1, "Name": "Yoga"},
                {"Id": 2, "Name": "Pilates"},
            ],
            "Total": 50,
            "Offset": 10,
        }
        qr = QueryResponse.from_dict(data, ServiceResponse)
        assert qr.total == 50
        assert qr.offset == 10
        assert len(qr.results) == 2
        assert qr.results[0].name == "Yoga"
        assert qr.results[1].id == 2

    def test_from_dict_empty_results(self):
        data = {"Results": [], "Total": 0, "Offset": 0}
        qr = QueryResponse.from_dict(data, ServiceResponse)
        assert qr.total == 0
        assert qr.offset == 0
        assert qr.results == []

    def test_from_dict_defaults_offset_and_total(self):
        data = {"Results": [{"Id": 1, "Name": "X"}]}
        qr = QueryResponse.from_dict(data, ServiceResponse)
        assert qr.offset == 0
        assert qr.total == 1  # len(items) when Total missing

    def test_from_dict_meta(self):
        data = {"Results": [], "Total": 0, "Offset": 0, "Meta": {"Key": "Value"}}
        qr = QueryResponse.from_dict(data, ServiceResponse)
        assert qr.meta == {"Key": "Value"}


# ---------------------------------------------------------------------------
# CompanyResponse
# ---------------------------------------------------------------------------


class TestCompanyResponse:
    def test_from_dict_uuid_parsing(self):
        d = {
            "Id": COMPANY_UUID_STR,
            "Name": "Spa & Wellness AB",
            "OrganisationNumber": "556123-4567",
            "TypeId": 3,
            "Street1": "Kungsgatan 1",
            "ZipCode": "11122",
            "City": "Stockholm",
            "CountryId": "SE",
            "Phone": "+46812345678",
            "Email": "info@spa.se",
            "SitePath": "spa-wellness",
            "Active": True,
        }
        c = CompanyResponse.from_dict(d)
        assert isinstance(c.id, UUID)
        assert c.id == COMPANY_UUID
        assert c.name == "Spa & Wellness AB"
        assert c.organisation_number == "556123-4567"
        assert c.city == "Stockholm"
        assert c.country_id == "SE"
        assert c.active is True

    def test_from_dict_defaults_when_empty(self):
        c = CompanyResponse.from_dict({})
        assert c.id is None
        assert c.name is None
        assert c.rating_score is None
        assert c.custom_fields == []

    def test_from_dict_parses_rating_score(self):
        d = {
            "Id": COMPANY_UUID_STR,
            "RatingScore": {"Score": 4.7, "Count": 120},
        }
        c = CompanyResponse.from_dict(d)
        assert c.rating_score is not None
        assert c.rating_score.score == 4.7
        assert c.rating_score.count == 120

    def test_company_type_response(self):
        d = {"Id": 5, "Name": "Gym", "Description": "Fitness centers"}
        ct = CompanyTypeResponse.from_dict(d)
        assert ct.id == 5
        assert ct.name == "Gym"
        assert ct.description == "Fitness centers"

    def test_company_type_response_empty(self):
        ct = CompanyTypeResponse.from_dict({})
        assert ct.id is None
        assert ct.name is None


# ---------------------------------------------------------------------------
# RebateCodeResponse
# ---------------------------------------------------------------------------


class TestRebateCodeResponse:
    def test_from_dict_full(self):
        d = {
            "Id": 7,
            "CompanyId": COMPANY_UUID_STR,
            "RebateCodeSign": "SUMMER26",
            "RebateCodeTypeId": 1,
            "RebateCodeValue": 20.0,
            "ValidFrom": "2026-06-01",
            "ValidTo": "2026-08-31",
            "MaxNumberOfUses": 100,
            "MaxNumberOfUsesPerCustomer": 1,
            "CurrencyId": "SEK",
            "RemainingUses": 98,
            "Active": True,
        }
        r = RebateCodeResponse.from_dict(d)
        assert r.id == 7
        assert isinstance(r.company_id, UUID)
        assert r.company_id == COMPANY_UUID
        assert r.rebate_code_sign == "SUMMER26"
        assert r.rebate_code_value == 20.0
        assert r.valid_from is not None
        assert r.valid_from.year == 2026
        assert r.valid_from.month == 6
        assert r.valid_to.month == 8
        assert r.remaining_uses == 98

    def test_from_dict_empty(self):
        r = RebateCodeResponse.from_dict({})
        assert r.id is None
        assert r.company_id is None
        assert r.valid_from is None
        assert r.valid_to is None
        assert r.days_of_week == []
        assert r.active is True

    def test_status_response(self):
        d = {"Id": 2, "Name": "Active"}
        s = RebateCodeStatusResponse.from_dict(d)
        assert s.id == 2
        assert s.name == "Active"

    def test_type_response(self):
        d = {"Id": 1, "Name": "Percentage", "Description": "Discount by %"}
        t = RebateCodeTypeResponse.from_dict(d)
        assert t.id == 1
        assert t.name == "Percentage"
        assert t.description == "Discount by %"


# ---------------------------------------------------------------------------
# CustomerResponse
# ---------------------------------------------------------------------------


class TestCustomerResponse:
    def test_from_dict_full(self):
        d = {
            "Id": CUSTOMER_UUID_STR,
            "UserId": COMPANY_UUID_STR,
            "Firstname": "Erik",
            "Lastname": "Nilsson",
            "Email": "erik@example.com",
            "Phone": "+46701112233",
            "PersonalIdentityNumber": "850101-1234",
            "SubscribedToNewsletter": True,
            "Visible": True,
            "Created": "2025-01-10T08:00:00Z",
        }
        c = CustomerResponse.from_dict(d)
        assert isinstance(c.id, UUID)
        assert c.id == CUSTOMER_UUID
        assert c.firstname == "Erik"
        assert c.lastname == "Nilsson"
        assert c.email == "erik@example.com"
        assert c.subscribed_to_newsletter is True
        assert c.created is not None

    def test_from_dict_defaults_when_empty(self):
        c = CustomerResponse.from_dict({})
        assert c.id is None
        assert c.subscribed_to_newsletter is False
        assert c.visible is True
        assert c.custom_fields == []
        assert c.comments == []

    def test_from_dict_parses_invoice_address(self):
        d = {
            "Id": CUSTOMER_UUID_STR,
            "InvoiceAddress": {
                "Street": "Main St 1",
                "City": "Gothenburg",
                "ZipCode": "41234",
                "CountryId": "SE",
            },
        }
        c = CustomerResponse.from_dict(d)
        assert c.invoice_address is not None
        assert c.invoice_address.city == "Gothenburg"

    def test_customer_article_response(self):
        d = {
            "Id": 10,
            "ArticleId": 3,
            "CustomerId": CUSTOMER_UUID_STR,
            "StatusId": 1,
            "Created": "2025-05-01T00:00:00Z",
        }
        ca = CustomerArticleResponse.from_dict(d)
        assert ca.id == 10
        assert ca.article_id == 3
        assert isinstance(ca.customer_id, UUID)
        assert ca.created is not None


# ---------------------------------------------------------------------------
# BillingMethodResponse
# ---------------------------------------------------------------------------


class TestBillingMethodResponse:
    def test_from_dict(self):
        d = {"Id": 1, "Name": "Invoice", "Description": "Payment by invoice"}
        bm = BillingMethodResponse.from_dict(d)
        assert bm.id == 1
        assert bm.name == "Invoice"
        assert bm.description == "Payment by invoice"

    def test_from_dict_empty(self):
        bm = BillingMethodResponse.from_dict({})
        assert bm.id is None
        assert bm.name is None
        assert bm.description is None

    def test_company_invoice_response(self):
        d = {
            "Id": 500,
            "CompanyId": COMPANY_UUID_STR,
            "StatusId": 1,
            "Status": "Paid",
            "Total": 1299.0,
            "Currency": "SEK",
            "Created": "2026-01-01T00:00:00Z",
            "InvoiceLines": [
                {"Id": 1, "Description": "Monthly plan", "Quantity": 1.0, "UnitPrice": 1299.0}
            ],
        }
        inv = CompanyInvoiceResponse.from_dict(d)
        assert inv.id == 500
        assert isinstance(inv.company_id, UUID)
        assert inv.total == 1299.0
        assert inv.currency == "SEK"
        assert len(inv.invoice_lines) == 1
        assert inv.invoice_lines[0].description == "Monthly plan"


# ---------------------------------------------------------------------------
# Common models
# ---------------------------------------------------------------------------


class TestCommonModels:
    def test_country_response(self):
        d = {"Id": "SE", "Name": "Sweden", "Currency": "SEK"}
        c = CountryResponse.from_dict(d)
        assert c.id == "SE"
        assert c.name == "Sweden"
        assert c.currency == "SEK"

    def test_currency_response(self):
        d = {"Id": "SEK", "Name": "Swedish Krona", "CurrencySign": "kr", "Active": True}
        c = CurrencyResponse.from_dict(d)
        assert c.id == "SEK"
        assert c.currency_sign == "kr"
        assert c.active is True

    def test_custom_field_value(self):
        d = {"Id": 3, "Column": "CustomField3", "Value": "hello"}
        cf = CustomFieldValue.from_dict(d)
        assert cf.id == 3
        assert cf.column == "CustomField3"
        assert cf.value == "hello"

    def test_invoice_address(self):
        d = {
            "Street": "Vasagatan 2",
            "City": "Malmö",
            "ZipCode": "21122",
            "CountryId": "SE",
            "Name": "AB Example",
        }
        ia = InvoiceAddress.from_dict(d)
        assert ia.street == "Vasagatan 2"
        assert ia.city == "Malmö"
        assert ia.name == "AB Example"


# ---------------------------------------------------------------------------
# ArticleResponse
# ---------------------------------------------------------------------------


class TestArticleResponse:
    def test_from_dict_full(self):
        d = {
            "Id": 11,
            "Name": "Gift Card 500",
            "Description": "A gift card worth 500 SEK",
            "ArticleTypeId": 2,
            "Price": 500.0,
            "CurrencyId": "SEK",
            "Duration": 365,
            "Active": True,
            "ServiceIds": [1, 2, 3],
        }
        a = ArticleResponse.from_dict(d)
        assert a.id == 11
        assert a.name == "Gift Card 500"
        assert a.price == 500.0
        assert a.duration == 365
        assert a.service_ids == [1, 2, 3]

    def test_from_dict_empty(self):
        a = ArticleResponse.from_dict({})
        assert a.id is None
        assert a.active is True
        assert a.service_ids == []

    def test_article_type_response(self):
        d = {"Id": 1, "Name": "Gift Card", "Description": "Physical or digital gift cards"}
        at = ArticleTypeResponse.from_dict(d)
        assert at.id == 1
        assert at.name == "Gift Card"


# ---------------------------------------------------------------------------
# ResourceResponse
# ---------------------------------------------------------------------------


class TestResourceModels:
    def test_resource_response_from_dict(self):
        d = {
            "Id": 42,
            "Name": "John Smith",
            "Description": "Senior therapist",
            "Active": True,
            "Color": "#FF5733",
            "Email": "john@spa.se",
            "EmailNotification": True,
        }
        r = ResourceResponse.from_dict(d)
        assert r.id == 42
        assert r.name == "John Smith"
        assert r.email == "john@spa.se"
        assert r.email_notification is True

    def test_resource_response_empty(self):
        r = ResourceResponse.from_dict({})
        assert r.id is None
        assert r.active is True
        assert r.custom_fields == []

    def test_resource_type_response(self):
        d = {
            "Id": 1,
            "Name": "Therapist",
            "Description": "Massage therapists",
            "Active": True,
            "Resources": [
                {"Id": 7, "Name": "John Smith"}
            ],
        }
        rt = ResourceTypeResponse.from_dict(d)
        assert rt.id == 1
        assert rt.name == "Therapist"
        assert len(rt.resources) == 1
        assert rt.resources[0].id == 7
        assert rt.resources[0].name == "John Smith"


# ---------------------------------------------------------------------------
# SupportCaseResponse
# ---------------------------------------------------------------------------


class TestSupportModels:
    def test_support_case_response_full(self):
        d = {
            "Id": 9,
            "CompanyId": COMPANY_UUID_STR,
            "Title": "Booking issue",
            "Description": "Cannot cancel booking",
            "CaseTypeId": 1,
            "Active": True,
            "Created": "2026-01-05T09:00:00Z",
        }
        sc = SupportCaseResponse.from_dict(d)
        assert sc.id == 9
        assert isinstance(sc.company_id, UUID)
        assert sc.title == "Booking issue"
        assert sc.active is True
        assert sc.created is not None

    def test_support_case_empty(self):
        sc = SupportCaseResponse.from_dict({})
        assert sc.id is None
        assert sc.active is True
        assert sc.comments == []
        assert sc.attachments == []

    def test_support_case_status_response(self):
        d = {"Id": 1, "Name": "Open", "Description": "Newly created", "Color": "#00FF00"}
        s = SupportCaseStatusResponse.from_dict(d)
        assert s.id == 1
        assert s.name == "Open"
        assert s.color == "#00FF00"


# ---------------------------------------------------------------------------
# CompanyLicenseResponse / CompanyTrialResponse
# ---------------------------------------------------------------------------


class TestLicenseModels:
    def test_company_license_response(self):
        d = {
            "Id": 20,
            "CompanyId": COMPANY_UUID_STR,
            "TypeId": 3,
            "TypeName": "Professional",
            "ValidFrom": "2026-01-01T00:00:00Z",
            "ValidTo": "2027-01-01T00:00:00Z",
            "Active": True,
        }
        lic = CompanyLicenseResponse.from_dict(d)
        assert lic.id == 20
        assert isinstance(lic.company_id, UUID)
        assert lic.type_name == "Professional"
        assert lic.active is True
        assert lic.valid_from is not None

    def test_company_trial_response(self):
        d = {
            "Id": 5,
            "CompanyId": COMPANY_UUID_STR,
            "TrialTypeId": 1,
            "TrialType": "Premium trial",
            "Started": "2026-02-01T00:00:00Z",
            "ValidTo": "2026-03-01T00:00:00Z",
            "Active": True,
        }
        trial = CompanyTrialResponse.from_dict(d)
        assert trial.id == 5
        assert trial.trial_type == "Premium trial"
        assert trial.active is True
        assert trial.started is not None


# ---------------------------------------------------------------------------
# CustomFieldResponse / CustomFieldValidationResponse
# ---------------------------------------------------------------------------


class TestCustomFieldModels:
    def test_custom_field_response_full(self):
        d = {
            "Id": 1,
            "Name": "Allergy info",
            "Description": "Do you have any allergies?",
            "Datatype": "TextBox",
            "IsMandatory": True,
            "MaxLength": 500,
            "IsPublic": True,
            "Active": True,
        }
        cf = CustomFieldResponse.from_dict(d)
        assert cf.id == 1
        assert cf.name == "Allergy info"
        assert cf.is_mandatory is True
        assert cf.max_length == 500
        assert cf.datatype == "TextBox"

    def test_custom_field_response_empty(self):
        cf = CustomFieldResponse.from_dict({})
        assert cf.id is None
        assert cf.is_mandatory is False
        assert cf.is_public is True
        assert cf.values == []

    def test_custom_field_validation_response(self):
        d = {"Id": 3, "Name": "Email pattern", "RegExCode": r"^[\w.]+@[\w.]+$"}
        v = CustomFieldValidationResponse.from_dict(d)
        assert v.id == 3
        assert v.name == "Email pattern"
        assert v.reg_ex_code is not None


# ---------------------------------------------------------------------------
# HomepageImageResponse
# ---------------------------------------------------------------------------


class TestHomepageModels:
    def test_homepage_image_response(self):
        d = {
            "Id": 8,
            "Title": "Front entrance",
            "Description": "Our beautiful entrance",
            "ImageUrl": "https://example.com/image.jpg",
        }
        img = HomepageImageResponse.from_dict(d)
        assert img.id == 8
        assert img.title == "Front entrance"
        assert img.image_url == "https://example.com/image.jpg"

    def test_homepage_image_empty(self):
        img = HomepageImageResponse.from_dict({})
        assert img.id is None
        assert img.title is None

    def test_homepage_settings_response(self):
        d = {
            "Id": 1,
            "CompanyId": COMPANY_UUID_STR,
            "EnableHomepage": True,
            "ShowRating": False,
            "Heading": "Welcome to our spa",
        }
        s = HomepageSettingsResponse.from_dict(d)
        assert s.id == 1
        assert isinstance(s.company_id, UUID)
        assert s.enable_homepage is True
        assert s.show_rating is False
        assert s.heading == "Welcome to our spa"

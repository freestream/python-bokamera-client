# bokamera

Typed Python 3.13 client library for the [BokaMera](https://www.bokamera.se) booking API.

## Installation

```bash
pip install httpx
pip install -e .
```

## Quick start

```python
from bokamera import BokaMeraClient
from datetime import datetime

with BokaMeraClient(api_key="your-api-key", company_id="your-company-uuid") as client:
    services = client.services.list(active=True, include_prices=True)
    for svc in services:
        print(svc.name, svc.duration)
```

## Authentication

All requests require an API key sent via the `x-api-key` header. The key is
created in the BokaMera admin panel.

```python
client = BokaMeraClient(
    api_key="your-api-key",
    company_id="your-company-uuid",  # set as default on all requests
)
```

`company_id` is optional at initialization but required by most endpoints — if
provided here it does not need to be passed on every call.

---

## Resources

The client exposes 19 resource namespaces:

| Namespace | Description |
|---|---|
| `client.bookings` | Bookings, booking log, booking queue and reports |
| `client.services` | Services, prices and available times |
| `client.resources` | Resources, resource types and time exceptions |
| `client.schedules` | Date schedules and recurring schedules |
| `client.customers` | Customers, comments and customer articles |
| `client.companies` | Companies, types, coordinates and administrators |
| `client.users` | User profile, agreements and favourites |
| `client.billing` | Billing, payment settings, Stripe and Qvickly |
| `client.articles` | Articles and article types |
| `client.rebate_codes` | Rebate codes, types, transactions and price calculation |
| `client.custom_fields` | Custom fields, slots and validation rules |
| `client.licenses` | Licenses, license types, plans and trial periods |
| `client.homepage` | Homepage settings, images, widget and news |
| `client.support` | Support cases, comments and attachments |
| `client.webhooks` | Webhook endpoints |
| `client.gdpr` | GDPR export and inactive customers |
| `client.eaccounting` | Visma eEkonomi integration |
| `client.codelock` | Code lock integrations (9 providers) |
| `client.system` | Version, settings, countries, currencies and more |

---

## Examples

### Services and available times

```python
from bokamera import BokaMeraClient
from datetime import datetime

with BokaMeraClient(api_key="...", company_id="...") as client:

    # List active services with prices and resources
    services = client.services.list(
        active=True,
        include_prices=True,
        include_resources=True,
    )

    # Get available times for a service
    available = client.services.get_available_times(
        service_id=42,
        from_=datetime(2026, 4, 1),
        to=datetime(2026, 4, 8),
    )

    for slot in available.times:
        print(f"{slot.from_} — {slot.free_spots} spots available")

    # Calculate price with rebate code
    price = client.services.calculate_price(
        service_id=42,
        rebate_code_ids=[101],
        quantities=[{"Id": 1, "Quantity": 2}],
    )
    print(f"Total price: {price.price}")
```

### Create and manage bookings

```python
from bokamera import BokaMeraClient, BokaMeraValidationError
from bokamera.models import PaymentOption
from datetime import datetime

with BokaMeraClient(api_key="...", company_id="...") as client:

    # Create a booking
    booking = client.bookings.create(
        from_=datetime(2026, 4, 2, 10, 0),
        to=datetime(2026, 4, 2, 11, 0),
        service_id=42,
        customer={
            "Firstname": "Anna",
            "Lastname": "Svensson",
            "Email": "anna@example.com",
            "Phone": "0701234567",
        },
        send_email_confirmation=True,
        payment_option=PaymentOption.BOOK_WITHOUT_PAYMENT,
    )
    print(f"Booking created: #{booking.id}")

    # List bookings for a period
    result = client.bookings.list(
        booking_start=datetime(2026, 4, 1),
        booking_end=datetime(2026, 4, 30),
        include_resources=True,
        take=50,
    )
    print(f"{result.total} bookings in total")

    # Approve a reserved booking
    client.bookings.approve(booking.id)

    # Mark as paid
    client.bookings.mark_as_paid(booking.id, comment="Paid via Swish")

    # Cancel booking
    client.bookings.delete(
        booking.id,
        send_email_confirmation=True,
        unbooked_comments="Customer cancelled",
    )
```

### Customers

```python
from bokamera.models import InvoiceAddress

with BokaMeraClient(api_key="...", company_id="...") as client:

    # Search customers
    customers = client.customers.list(search="Anna", include_custom_field_values=True)

    # Create customer
    customer = client.customers.create(
        firstname="Erik",
        lastname="Lindqvist",
        email="erik@example.com",
        phone="0709876543",
        invoice_address=InvoiceAddress(
            street="Storgatan 1",
            zip_code="111 22",
            city="Stockholm",
            country_id="SE",
        ),
    )

    # Add comment
    client.customers.add_comment(
        customer.id,
        comments="Prefers morning bookings.",
    )
```

### Resources and schedules

```python
from datetime import date, time, datetime

with BokaMeraClient(api_key="...", company_id="...") as client:

    # List resources
    resources = client.resources.list(active=True, include_exceptions=True)

    # Create resource
    resource = client.resources.create(
        name="Treatment room 1",
        color="#4A90D9",
        email_notification=True,
    )

    # Add time exception (closed)
    client.resources.create_exception(
        from_=datetime(2026, 6, 20),
        to=datetime(2026, 6, 27),
        resource_ids=[resource.id],
        reason_text="Holiday",
        block_time=True,
    )

    # Create a recurring schedule (Mon–Fri, 08:00–17:00)
    client.schedules.create_recurring(
        name="Office hours",
        time_interval=60,
        valid_from=date(2026, 1, 1),
        valid_to=date(2026, 12, 31),
        start_time=time(8, 0),
        end_time=time(17, 0),
        days_of_week=[1, 2, 3, 4, 5],  # 1=Monday, 7=Sunday
        resources=[{"Id": str(resource.id)}],
    )
```

### Rebate codes

```python
from datetime import date

with BokaMeraClient(api_key="...", company_id="...") as client:

    # Create rebate code (10% discount)
    code = client.rebate_codes.create(
        rebate_code_type_id=2,      # percentage discount
        rebate_code_value=10.0,
        rebate_code_sign="SUMMER26",
        valid_from=date(2026, 6, 1),
        valid_to=date(2026, 8, 31),
        max_number_of_uses=100,
    )

    # Look up code at booking time
    found = client.rebate_codes.get_by_sign(
        company_id="...",
        rebate_code_sign="SUMMER26",
        service_id=42,
    )
    print(f"Discount: {found.rebate_code_value}%, remaining: {found.remaining_uses}")
```

### Billing

```python
with BokaMeraClient(api_key="...", company_id="...") as client:

    # Get invoices
    invoices = client.billing.list_invoices(include_invoice_lines=True)

    # Download invoice as PDF
    pdf_bytes = client.billing.get_invoice_pdf(invoice_id=42)
    with open("invoice.pdf", "wb") as f:
        f.write(pdf_bytes)

    # Configure Stripe webhook
    webhook = client.billing.create_stripe_webhook(
        url="https://my-app.example/webhooks/stripe",
        events=["payment_intent.succeeded", "payment_intent.payment_failed"],
    )
```

### GDPR

```python
from datetime import date

with BokaMeraClient(api_key="...", company_id="...") as client:

    # Export all data for a customer
    data = client.gdpr.get_customer_data(
        customer_id="customer-uuid",
        company_id="company-uuid",
    )
    print(data.bookings, data.message_log)

    # List customers who have not booked in 2 years
    inactive = client.gdpr.list_inactive_customers(
        inactive_since=date(2024, 1, 1),
        include_customer_information=True,
    )

    # Delete inactive customers (GDPR cleanup)
    client.gdpr.delete_inactive_customers(inactive_since=date(2024, 1, 1))
```

### Code lock integrations

```python
with BokaMeraClient(api_key="...", company_id="...") as client:

    # Activate Accessy
    client.codelock.create_accessy(
        client_id="accessy-client-id",
        client_secret="accessy-client-secret",
    )

    # Activate Zesec and unlock manually
    client.codelock.create_zesec(phone_number="+46701234567", password="...")
    client.codelock.zesec_unlock(booking_id=1234)

    # Check general settings
    settings = client.codelock.get_settings(include_options=True)
    print(f"Active system: {settings.code_lock_system_name}")
```

### Visma eEkonomi

```python
with BokaMeraClient(api_key="...", company_id="...") as client:

    # Check connection
    token = client.eaccounting.check_connection()

    # Create invoice from booking
    invoice = client.eaccounting.create_invoice(
        booking_id=1234,
        invoice_customer_name="Acme AB",
        send_type="Email",
        terms_of_payment_id="30-days",
    )

    # List invoice drafts
    drafts = client.eaccounting.list_invoice_drafts(booking_id=1234)
```

### Homepage and news

```python
with BokaMeraClient(api_key="...", company_id="...") as client:

    # Update widget theme
    client.homepage.update_widget_settings(
        primary_color="#E87722",
        dark_theme=False,
        enable_direct_booking=True,
    )

    # Create news item
    client.homepage.create_news(
        heading="Summer holiday",
        body="We are closed weeks 28–30.",
        from_date="2026-07-06",
        to_date="2026-07-26",
    )
```

---

## Error handling

```python
from bokamera import (
    BokaMeraClient,
    BokaMeraAuthError,
    BokaMeraNotFoundError,
    BokaMeraRateLimitError,
    BokaMeraValidationError,
)

with BokaMeraClient(api_key="...", company_id="...") as client:
    try:
        booking = client.bookings.create(
            from_=datetime(2026, 4, 2, 10, 0),
            to=datetime(2026, 4, 2, 11, 0),
            service_id=42,
            customer={"Email": "invalid-email"},
        )
    except BokaMeraValidationError as e:
        print(f"Validation error: {e.message}")
    except BokaMeraAuthError:
        print("Invalid API key")
    except BokaMeraRateLimitError:
        print("Too many requests — wait and try again")
    except BokaMeraNotFoundError as e:
        print(f"Resource not found: {e.message}")
```

| Exception | HTTP status |
|---|---|
| `BokaMeraValidationError` | 400 |
| `BokaMeraAuthError` | 401 |
| `BokaMeraForbiddenError` | 403 |
| `BokaMeraNotFoundError` | 404 |
| `BokaMeraRateLimitError` | 429 |
| `BokaMeraHTTPError` | other 4xx/5xx |

---

## Data models

All responses are returned as `@dataclass` instances with full type annotations.
Dates and times are `datetime`/`date`/`time` objects, IDs are `UUID` or `int`
depending on the API.

```python
from bokamera.models import BookingResponse, ServiceResponse, CustomerResponse

booking: BookingResponse = client.bookings.create(...)
print(booking.id)          # int
print(booking.from_)       # datetime
print(booking.company_id)  # UUID
print(booking.customer)    # BookingCustomer | None
```

Paginated lists are returned as `QueryResponse[T]`:

```python
from bokamera.models import QueryResponse, BookingResponse

result: QueryResponse[BookingResponse] = client.bookings.list(take=25)
print(result.total)    # total number of results
print(result.offset)   # offset
print(result.results)  # list[BookingResponse]
```

---

## Requirements

- Python 3.13+
- [httpx](https://www.python-httpx.org/) >= 0.27

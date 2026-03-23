"""JSON serialisation support for BokaMera response models."""

from __future__ import annotations

import dataclasses
import json
from datetime import date, datetime
from uuid import UUID


class BokaMeraEncoder(json.JSONEncoder):
    """JSON encoder that handles BokaMera response models.

    Supports:
    - Dataclass instances (recursively converted to dicts)
    - :class:`~datetime.datetime` → ISO 8601 string
    - :class:`~datetime.date` → ISO 8601 string
    - :class:`~uuid.UUID` → string

    Usage::

        import json
        from bokamera import BokaMeraClient, BokaMeraEncoder

        with BokaMeraClient(api_key="...", company_id="...") as client:
            result = client.bookings.list(take=10)
            print(json.dumps(result, cls=BokaMeraEncoder, indent=2))
    """

    def default(self, obj: object) -> object:
        if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
            return dataclasses.asdict(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)

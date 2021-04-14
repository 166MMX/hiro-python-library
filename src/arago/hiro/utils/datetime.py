from datetime import datetime, timezone
from typing import Optional


def timestamp_ms_to_datetime(value: Optional[int] = None) -> Optional[datetime]:
    if value is None:
        return None
    return datetime.fromtimestamp(value / 1e3, tz=timezone.utc)


def datetime_to_timestamp_ms(value: Optional[datetime] = None) -> Optional[int]:
    if value is None:
        return None
    if value.tzinfo is None:
        raise ValueError('tzinfo is required')
    return int(value.timestamp() * 1e3)

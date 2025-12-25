from datetime import datetime, timezone


def unix_to_utc_datetime(timestamp: float) -> datetime:
    """
    Convert Unix timestamp to UTC datetime object.
    """
    return datetime.fromtimestamp(timestamp, tz=timezone.utc)


def utc_now() -> datetime:
    """
    Get current UTC time.
    """
    return datetime.now(timezone.utc)

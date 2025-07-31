"""Date related services."""

from datetime import UTC, datetime


def utc_now():
    """Returns current date.

    Returns:
        datetime: datetime.now(UTC)
    """
    return datetime.now(UTC)

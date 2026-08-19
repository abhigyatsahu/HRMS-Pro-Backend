from datetime import date, datetime, timedelta

from django.utils import timezone


def now() -> datetime:
    """
    Return the current timezone-aware datetime.
    """

    return timezone.now()


def today() -> date:
    """
    Return today's date in the active Django timezone.
    """

    return timezone.localdate()


def start_of_day(
    value: date | datetime | None = None,
) -> datetime:
    """
    Return the beginning of the given day.
    """

    if value is None:
        value = timezone.localdate()

    if isinstance(value, datetime):
        value = timezone.localtime(value).date()

    return timezone.make_aware(
        datetime.combine(
            value,
            datetime.min.time(),
        )
    )


def end_of_day(
    value: date | datetime | None = None,
) -> datetime:
    """
    Return the end of the given day.
    """

    if value is None:
        value = timezone.localdate()

    if isinstance(value, datetime):
        value = timezone.localtime(value).date()

    return (
        start_of_day(value)
        + timedelta(days=1)
        - timedelta(microseconds=1)
    )
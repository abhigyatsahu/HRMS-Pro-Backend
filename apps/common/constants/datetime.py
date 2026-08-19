"""
Date and time related constants used throughout HRMS.

Database datetime values should remain timezone-aware.
API datetime values should follow ISO 8601.
Display formats are intended for human-readable output.
"""


class DateTimeFormat:
    """
    Standard date and time formats.
    """

    DATE = "%Y-%m-%d"

    TIME = "%H:%M:%S"

    SHORT_TIME = "%H:%M"

    DATETIME = "%Y-%m-%dT%H:%M:%S"

    DISPLAY_DATE = "%d-%m-%Y"

    DISPLAY_TIME = "%I:%M %p"

    DISPLAY_DATETIME = "%d-%m-%Y %I:%M %p"

    MONTH = "%Y-%m"

    DISPLAY_MONTH = "%B %Y"

    WEEKDAY = "%A"

    SHORT_WEEKDAY = "%a"
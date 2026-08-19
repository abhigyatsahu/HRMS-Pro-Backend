"""
Cookie-related constants used throughout HRMS.

This module contains only fixed cookie names and
cookie configuration values.

Cookie handling logic must remain in the authentication
/API layer.
"""


class CookieName:
    """
    Names of cookies used by the application.
    """

    ACCESS_TOKEN = "access_token"

    REFRESH_TOKEN = "refresh_token"

    CSRF_TOKEN = "csrftoken"


class CookiePath:
    """
    Cookie path configuration.
    """

    ROOT = "/"

    AUTH = "/api/auth/"


class CookieSameSite:
    """
    SameSite cookie policies.
    """

    STRICT = "Strict"

    LAX = "Lax"

    NONE = "None"


class CookieMaxAge:
    """
    Cookie lifetime values in seconds.
    """

    ONE_MINUTE = 60

    FIVE_MINUTES = 5 * ONE_MINUTE

    FIFTEEN_MINUTES = 15 * ONE_MINUTE

    ONE_HOUR = 60 * ONE_MINUTE

    ONE_DAY = 24 * ONE_HOUR

    SEVEN_DAYS = 7 * ONE_DAY

    THIRTY_DAYS = 30 * ONE_DAY
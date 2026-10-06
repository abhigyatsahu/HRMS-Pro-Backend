from django.conf import settings
from drf_spectacular.extensions import (
    OpenApiAuthenticationExtension,
)


class CookieJWTAuthenticationScheme(
    OpenApiAuthenticationExtension
):
    """
    OpenAPI authentication scheme for
    CookieJWTAuthentication.
    """

    target_class = (
        "apps.accounts.authentication.CookieJWTAuthentication"
    )

    name = "CookieJWTAuthentication"

    def get_security_definition(
        self,
        auto_schema,
    ):
        cookie_name = getattr(settings, "JWT_ACCESS_COOKIE", "access_token")
        return {
            "type": "apiKey",
            "in": "cookie",
            "name": cookie_name,
            "description": (
                f"JWT access token stored in the "
                f"{cookie_name} HTTP cookie."
            ),
        }
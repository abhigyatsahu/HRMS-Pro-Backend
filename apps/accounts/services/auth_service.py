from django.conf import settings


def set_access_cookie(
    response,
    token,
):
    response.set_cookie(
        key=settings.JWT_ACCESS_COOKIE,
        value=str(token),
        max_age=settings.JWT_COOKIE_ACCESS_MAX_AGE,
        httponly=True,
        secure=settings.JWT_COOKIE_SECURE,
        samesite=settings.JWT_COOKIE_SAMESITE,
        path="/",
    )


def set_refresh_cookie(
    response,
    token,
):
    response.set_cookie(
        key=settings.JWT_REFRESH_COOKIE,
        value=str(token),
        max_age=settings.JWT_COOKIE_REFRESH_MAX_AGE,
        httponly=True,
        secure=settings.JWT_COOKIE_SECURE,
        samesite=settings.JWT_COOKIE_SAMESITE,
        path="/",
    )


def clear_auth_cookies(response):
    response.delete_cookie(
        key=settings.JWT_ACCESS_COOKIE,
        path="/",
        samesite=settings.JWT_COOKIE_SAMESITE,
    )

    response.delete_cookie(
        key=settings.JWT_REFRESH_COOKIE,
        path="/",
        samesite=settings.JWT_COOKIE_SAMESITE,
    )
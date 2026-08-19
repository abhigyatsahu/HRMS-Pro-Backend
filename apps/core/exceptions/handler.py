from rest_framework.response import Response
from rest_framework.views import exception_handler

from apps.common.utils import error_payload

from .base import HRMSException

def _get_error_message(status_code):
    messages = {
        400: "Invalid request.",
        401: "Authentication required.",
        403: "Permission denied.",
        404: "Resource not found.",
        405: "Method not allowed.",
        409: "Resource conflict.",
        429: "Too many requests.",
    }

    return messages.get(
        status_code,
        "Request failed.",
    )

def custom_exception_handler(exc, context):
    """
    Global exception handler.
    """

    response = exception_handler(
        exc,
        context,
    )

    if isinstance(exc, HRMSException):
        return Response(
            error_payload(
                message=exc.message,
                errors={
                    "code": exc.code,
                },
            ),
            status=exc.status_code,
        )

    if response is not None:
        return Response(
            error_payload(
                message=_get_error_message(
                    response.status_code
                ),
                errors=response.data,
            ),
            status=response.status_code,
        )

    return Response(
        error_payload(
            message="Internal server error.",
            errors={},
        ),
        status=500,
    )
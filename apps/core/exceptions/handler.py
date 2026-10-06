import logging

from rest_framework.response import Response
from rest_framework.views import exception_handler

from apps.common.utils import error_payload

from .base import HRMSException


logger = logging.getLogger(__name__)


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

    # HRMS application exceptions
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

    # DRF handled exceptions
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

    # Unexpected / unhandled exception
    logger.exception(
        "Unhandled exception in API",
        exc_info=exc,
    )

    return Response(
        error_payload(
            message="Internal server error.",
            errors={},
        ),
        status=500,
    )
from .base import CommonException


class ExternalServiceException(CommonException):
    """
    Raised when an external dependency fails.
    """

    default_message = "External service unavailable."

    default_code = "external_service_error"
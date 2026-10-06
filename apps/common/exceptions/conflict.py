from apps.core.exceptions.base import HRMSException


class DuplicateResourceException(HRMSException):
    """
    Raised when an operation attempts to create
    a resource that already exists.
    """

    default_message = "Resource already exists."
    status_code = 409
    default_code = "duplicate_resource"
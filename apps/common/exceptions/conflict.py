from .base import CommonException


class DuplicateResourceException(CommonException):
    """
    Raised when an operation attempts to create
    a resource that already exists.
    """

    default_message = "Resource already exists."

    default_code = "duplicate_resource"
from rest_framework import status

from .base import HRMSException


class ValidationException(HRMSException):

    status_code = status.HTTP_400_BAD_REQUEST

    default_message = "Validation failed."

    default_code = "validation_error"
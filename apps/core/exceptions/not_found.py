from rest_framework import status

from .base import HRMSException


class NotFoundException(HRMSException):

    status_code = status.HTTP_404_NOT_FOUND

    default_message = "Resource not found."

    default_code = "not_found"
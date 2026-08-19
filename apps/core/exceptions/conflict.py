from rest_framework import status

from .base import HRMSException


class ConflictException(HRMSException):

    status_code = status.HTTP_409_CONFLICT

    default_message = "Conflict detected."

    default_code = "conflict"
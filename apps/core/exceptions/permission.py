from rest_framework import status

from .base import HRMSException


class PermissionException(HRMSException):

    status_code = status.HTTP_403_FORBIDDEN

    default_message = "Permission denied."

    default_code = "permission_denied"
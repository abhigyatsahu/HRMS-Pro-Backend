from rest_framework import status

from .base import HRMSException


class BusinessException(HRMSException):

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY

    default_message = "Business rule violated."

    default_code = "business_error"
from django.db import transaction
from rest_framework.generics import GenericAPIView

from .base import BaseAPIView


class BaseWriteAPIView(
    BaseAPIView,
    GenericAPIView,
):
    """
    Base class for all write APIs.
    """


    def dispatch(self, request, *args, **kwargs):
        """
        Wrap every write request
        inside a database transaction.
        """
        return super().dispatch(
            request,
            *args,
            **kwargs,
        )
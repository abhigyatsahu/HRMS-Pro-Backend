from rest_framework.generics import GenericAPIView

from apps.core.pagination import StandardPagination
from .base import BaseAPIView


class BaseReadAPIView(
    BaseAPIView,
    GenericAPIView,
):
    """
    Base class for all read APIs.
    """

    pagination_class = StandardPagination

    search_fields = ()

    ordering_fields = ()

    ordering = ()
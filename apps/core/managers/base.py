from django.db import models

from core.querysets.base import BaseQuerySet


class BaseManager(models.Manager.from_queryset(BaseQuerySet)):
    """
    Base manager shared across all models.
    """

    pass
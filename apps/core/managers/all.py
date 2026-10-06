from django.db import models

from apps.core.querysets import SoftDeleteQuerySet


class AllObjectsManager(
    models.Manager.from_queryset(
        SoftDeleteQuerySet
    )
):
    """
    Returns every record,
    including deleted ones.
    """

    pass
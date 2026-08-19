from django.db import models

from core.querysets.soft_delete import SoftDeleteQuerySet


class SoftDeleteManager(
    models.Manager.from_queryset(
        SoftDeleteQuerySet
    )
):
    """
    Default manager for soft deleted models.
    """

    def get_queryset(self):
        """
        Hide deleted records automatically.
        """

        return (
            super()
            .get_queryset()
            .not_deleted()
        )
from django.db import models

from apps.designations.querysets.designation import (
    DesignationQuerySet,
)


class DesignationManager(
    models.Manager.from_queryset(
        DesignationQuerySet
    )
):
    """
    Manager for Designation model.

    Excludes soft-deleted records by default.
    """

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .not_deleted()
        )
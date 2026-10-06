from django.db import models

from apps.organization.querysets.branch import (
    BranchQuerySet,
)


class BranchManager(
    models.Manager.from_queryset(
        BranchQuerySet
    )
):
    def get_queryset(self):
        return super().get_queryset().not_deleted()
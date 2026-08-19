from django.db import models
from django.utils import timezone

from core.managers.all import AllObjectsManager
from core.managers.soft_delete import SoftDeleteManager


class SoftDeleteModel(models.Model):

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
    )

    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()

        self.save(
            update_fields=[
                "is_deleted",
                "deleted_at",
            ]
        )

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None

        self.save(
            update_fields=[
                "is_deleted",
                "deleted_at",
            ]
        )
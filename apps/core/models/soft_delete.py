from django.db import models
from django.utils import timezone

from apps.core.managers.all import AllObjectsManager
from apps.core.managers.soft_delete import SoftDeleteManager


class SoftDeleteModel(models.Model):
    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Soft delete the instance."""

        self.is_deleted = True
        self.deleted_at = timezone.now()

        update_fields = [
            "is_deleted",
            "deleted_at",
        ]

        if hasattr(self, "updated_at"):
            self.updated_at = timezone.now()
            update_fields.append("updated_at")

        self.save(
            update_fields=update_fields,
            using=using,
        )

        return 1, {
            self._meta.label: 1,
        }

    def restore(self):
        """Restore the soft-deleted instance."""

        self.is_deleted = False
        self.deleted_at = None

        update_fields = [
            "is_deleted",
            "deleted_at",
        ]

        if hasattr(self, "updated_at"):
            self.updated_at = timezone.now()
            update_fields.append("updated_at")

        self.save(
            update_fields=update_fields,
        )

        return 1, {
            self._meta.label: 1,
        }
from django.utils import timezone

from .base import BaseQuerySet


class SoftDeleteQuerySet(BaseQuerySet):

    def deleted(self):
        return self.filter(
            is_deleted=True,
        )

    def not_deleted(self):
        return self.filter(
            is_deleted=False,
        )

    def delete(self):
        now = timezone.now()

        update_kwargs = {
            "is_deleted": True,
            "deleted_at": now,
        }

        if hasattr(self.model, "updated_at"):
            update_kwargs["updated_at"] = now

        rows_updated = self.update(
            **update_kwargs
        )

        return rows_updated, {
            self.model._meta.label: rows_updated,
        }

    def restore(self):
        update_kwargs = {
            "is_deleted": False,
            "deleted_at": None,
        }

        if hasattr(self.model, "updated_at"):
            update_kwargs["updated_at"] = timezone.now()

        rows_updated = self.update(
            **update_kwargs
        )

        return rows_updated, {
            self.model._meta.label: rows_updated,
        }

    def hard_delete(self):
        return super().delete()
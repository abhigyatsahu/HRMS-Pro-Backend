from django.utils import timezone

from .base import BaseQuerySet


class SoftDeleteQuerySet(BaseQuerySet):
    """
    QuerySet with soft delete support.
    """

    def deleted(self):
        """
        Return deleted records.
        """

        return self.filter(
            is_deleted=True
        )

    def not_deleted(self):
        """
        Return non-deleted records.
        """

        return self.filter(
            is_deleted=False
        )

    def soft_delete(self):
        """
        Soft delete all rows.
        """

        return self.update(
            is_deleted=True,
            deleted_at=timezone.now(),
        )

    def restore(self):
        """
        Restore deleted rows.
        """

        return self.update(
            is_deleted=False,
            deleted_at=None,
        )

    def hard_delete(self):
        """
        Permanently delete records.
        """

        return super().delete()
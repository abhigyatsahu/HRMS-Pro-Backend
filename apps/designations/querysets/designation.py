from django.db import models

from apps.core.querysets.soft_delete import SoftDeleteQuerySet


class DesignationQuerySet(SoftDeleteQuerySet):
    """
    QuerySet containing reusable Designation queries.
    """

    def active(self):
        return self.filter(
            is_active=True
        )

    def inactive(self):
        return self.filter(
            is_active=False
        )

    def for_organization(
        self,
        organization,
    ):
        return self.filter(
            organization=organization
        )

    def search(
        self,
        value,
    ):
        if not value:
            return self

        value = value.strip()

        if not value:
            return self

        return self.filter(
            models.Q(
                name__icontains=value
            )
            | models.Q(
                code__icontains=value
            )
            | models.Q(
                description__icontains=value
            )
        )
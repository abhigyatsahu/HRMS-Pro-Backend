from django.db import models
from apps.core.querysets.soft_delete import SoftDeleteQuerySet


class BranchQuerySet(SoftDeleteQuerySet):

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
        term,
    ):
        if not term:
            return self

        return self.filter(
            models.Q(name__icontains=term)
            | models.Q(code__icontains=term)
            | models.Q(city__icontains=term)
            | models.Q(state__icontains=term)
            | models.Q(email__icontains=term)
            | models.Q(phone__icontains=term)
        )
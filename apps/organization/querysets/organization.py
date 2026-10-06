from django.db import models
from apps.core.querysets.soft_delete import SoftDeleteQuerySet


class OrganizationQuerySet(SoftDeleteQuerySet):
    """
    QuerySet for Organization model.
    """

    def active(self):
        return self.filter(
            is_active=True,
        )

    def inactive(self):
        return self.filter(
            is_active=False,
        )

    def search(self, value):
        """
        Search organizations by name, code,
        legal name, email, or phone.
        """

        if not value:
            return self

        return self.filter(
            models.Q(name__icontains=value)
            | models.Q(code__icontains=value)
            | models.Q(
                legal_name__icontains=value
            )
            | models.Q(email__icontains=value)
            | models.Q(phone__icontains=value)
        )

    def ordered(self):
        """
        Return organizations in their
        standard ordering.
        """

        return self.order_by("name")
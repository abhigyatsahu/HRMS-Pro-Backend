from django.db import models

from apps.organization.querysets.organization import (
    OrganizationQuerySet,
)


class OrganizationManager(
    models.Manager.from_queryset(
        OrganizationQuerySet
    )
):
    """
    Manager for Organization model.
    """

    def get_queryset(self):
        return super().get_queryset().not_deleted()

    def get_by_uuid(self, organization_uuid):
        return self.get(
            uuid=organization_uuid,
        )
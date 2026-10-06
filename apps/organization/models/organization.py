import uuid

from django.db import models
from apps.core.models.soft_delete import SoftDeleteModel
from apps.organization.managers.organization import (
    OrganizationManager,
)
from apps.organization.querysets.organization import (
    OrganizationQuerySet,
)

class Organization(SoftDeleteModel):
    """
    Represents an HRMS organization/tenant.
    """

    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )


    name = models.CharField(
        max_length=200,
    )

    code = models.CharField(
        max_length=50,
        unique=True,
    )

    legal_name = models.CharField(
        max_length=250,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    website = models.URLField(
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    state = models.CharField(
        max_length=100,
        blank=True,
    )

    country = models.CharField(
        max_length=100,
        default="India",
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
    )

    logo = models.ImageField(
        upload_to="organizations/logos/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    objects = OrganizationManager()
    all_objects = models.Manager.from_queryset(OrganizationQuerySet)()

    class Meta:
        app_label = "organization"
        db_table = "organizations"
        ordering = ["name"]

    def __str__(self):
        return self.name
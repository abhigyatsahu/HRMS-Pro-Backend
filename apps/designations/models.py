import uuid

from django.db import models
from apps.core.models.soft_delete import SoftDeleteModel
from apps.organization.models import Organization
from apps.designations.managers import (
    DesignationManager,
)
from apps.designations.querysets.designation import (
    DesignationQuerySet,
)

class Designation(SoftDeleteModel):
    """
    Represents an employee designation within an organization.
    """
    objects = DesignationManager()
    all_objects = models.Manager.from_queryset(
        DesignationQuerySet
    )()

    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="designations",
    )

    name = models.CharField(
        max_length=150,
    )

    code = models.CharField(
        max_length=50,
    )

    description = models.TextField(
        blank=True,
    )

    level = models.PositiveIntegerField(
        default=1,
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


    class Meta:
        db_table = "designations"

        ordering = [
            "level",
            "name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "code",
                ],
                condition=models.Q(
                    is_deleted=False
                ),
                name=(
                    "unique_designation_code_per_organization"
                ),
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "is_active",
                ],
                name=(
                    "designation_org_active_idx"
                ),
            ),
        ]

    def __str__(self):
        return (
            f"{self.name} ({self.code})"
        )
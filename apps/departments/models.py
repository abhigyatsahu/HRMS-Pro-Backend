import uuid

from django.db import models
from apps.core.models.soft_delete import SoftDeleteModel
from apps.departments.managers import (
    DepartmentManager,
)
from apps.departments.managers.department import DepartmentQuerySet
from apps.organization.models import Organization


class Department(SoftDeleteModel):
    """
    Represents a department within an organization.
    """

    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="departments",
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

    objects = DepartmentManager()
    all_objects = models.Manager.from_queryset(DepartmentQuerySet)()

    class Meta:
        db_table = "departments"

        ordering = [
            "name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "code",
                ],
                name="unique_department_code_per_org",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "is_active",
                ],
                name="department_org_active_idx",
            ),
        ]

    def __str__(self):
        return self.name
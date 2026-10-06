import uuid

from django.db import models

from apps.core.models.timestamp import TimeStampedModel
from apps.core.models.soft_delete import SoftDeleteModel

from .organization import Organization
from ..managers.branch import BranchManager
from ..querysets.branch import BranchQuerySet


class Branch(SoftDeleteModel, TimeStampedModel):
    """
    Represents a branch/location belonging to an organization.
    """

    objects = BranchManager()
    all_objects = models.Manager.from_queryset(BranchQuerySet)()

    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="branches",
    )

    name = models.CharField(
        max_length=150,
    )

    code = models.CharField(
        max_length=50,
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

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta:
        app_label = "organization"
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "code",
                ],
                name="unique_branch_code_per_organization",
            ),
        ]

    def __str__(self):
        return f"{self.organization.code} - {self.name}"
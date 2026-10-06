
from django.db import transaction
from rest_framework.exceptions import NotFound

from apps.common.exceptions import (
    DuplicateResourceException,
    BusinessRuleException,
)
from apps.organization.models import (
    Branch,
    Organization,
)


class BranchService:
    """
    Business operations for Branch.
    """

    @staticmethod
    @transaction.atomic
    def create(validated_data):
        """
        Create a new branch.
        """
        data = validated_data.copy()

        organization_uuid = (
            data.pop(
                "organization_uuid"
            )
        )

        try:
            organization = Organization.objects.get(
                uuid=organization_uuid
            )
        except Organization.DoesNotExist:
            raise NotFound(f"Organization with uuid '{organization_uuid}' ")

        if not organization.is_active:
            raise BusinessRuleException(
                "Cannot create a branch for "
                "an inactive organization."
            )

        code = data["code"]

        if Branch.objects.filter(
            organization=organization,
            code=code,
        ).exists():
            raise DuplicateResourceException(
                f"Branch code '{code}' already "
                "exists for this organization."
            )

        return Branch.objects.create(
            organization=organization,
            **data,
        )

    @staticmethod
    @transaction.atomic
    def update(
            branch,
            validated_data,
    ):
        """
        Update an existing branch.
        """

        new_code = validated_data.get(
            "code"
        )

        if (
                new_code
                and new_code != branch.code
                and Branch.objects.filter(
            organization=branch.organization,
            code=new_code,
        )
                .exclude(
            pk=branch.pk
        )
                .exists()
        ):
            raise DuplicateResourceException(
                f"Branch code '{new_code}' already "
                "exists for this organization."
            )

        changed_fields = []

        for field, value in validated_data.items():

            if getattr(
                    branch,
                    field,
            ) != value:
                setattr(
                    branch,
                    field,
                    value,
                )

                changed_fields.append(
                    field
                )

        if changed_fields:
            changed_fields.append(
                "updated_at"
            )

            branch.save(
                update_fields=changed_fields
            )

        return branch

    @staticmethod
    @transaction.atomic
    def activate(branch):
        """
        Activate a branch.
        """

        if branch.is_active:
            return branch

        if not branch.organization.is_active:
            raise BusinessRuleException(
                "Cannot activate a branch belonging "
                "to an inactive organization."
            )

        branch.is_active = True

        branch.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        return branch

    @staticmethod
    @transaction.atomic
    def deactivate(branch):
        """
        Deactivate a branch.
        """

        if not branch.is_active:
            return branch

        branch.is_active = False

        branch.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        return branch
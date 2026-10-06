from django.db import transaction
from rest_framework.exceptions import NotFound

from apps.common.exceptions import (
    BusinessRuleException,
    DuplicateResourceException,
)
from apps.designations.models import Designation
from apps.organization.models import Organization


class DesignationService:
    """
    Business operations for Designation.
    """

    @staticmethod
    @transaction.atomic
    def create(validated_data):
        """
        Create a new designation.
        """

        data = validated_data.copy()

        organization_uuid = data.pop(
            "organization_uuid"
        )

        try:
            organization = Organization.objects.get(
                uuid=organization_uuid
            )
        except Organization.DoesNotExist:
            raise NotFound(
                f"Organization with uuid "
                f"'{organization_uuid}' not found."
            )

        if not organization.is_active:
            raise BusinessRuleException(
                "Cannot create a designation for "
                "an inactive organization."
            )

        code = data["code"]

        if Designation.objects.filter(
            organization=organization,
            code=code,
        ).exists():
            raise DuplicateResourceException(
                f"Designation code '{code}' already "
                "exists for this organization."
            )

        return Designation.objects.create(
            organization=organization,
            **data,
        )

    @staticmethod
    @transaction.atomic
    def update(
        designation,
        validated_data,
    ):
        """
        Update an existing designation.
        """

        new_code = validated_data.get(
            "code"
        )

        if (
            new_code
            and new_code != designation.code
            and Designation.objects.filter(
                organization=designation.organization,
                code=new_code,
            )
            .exclude(
                pk=designation.pk
            )
            .exists()
        ):
            raise DuplicateResourceException(
                f"Designation code '{new_code}' "
                "already exists for this organization."
            )

        changed_fields = []

        for field, value in validated_data.items():
            if getattr(
                designation,
                field,
            ) != value:
                setattr(
                    designation,
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

            designation.save(
                update_fields=changed_fields
            )

        return designation

    @staticmethod
    @transaction.atomic
    def activate(designation):
        """
        Activate a designation.
        """

        if designation.is_active:
            return designation

        if not designation.organization.is_active:
            raise BusinessRuleException(
                "Cannot activate a designation "
                "belonging to an inactive organization."
            )

        designation.is_active = True

        designation.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        return designation

    @staticmethod
    @transaction.atomic
    def deactivate(designation):
        """
        Deactivate a designation.
        """

        if not designation.is_active:
            return designation

        designation.is_active = False

        designation.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        return designation

    @staticmethod
    @transaction.atomic
    def delete(designation):
        """
        Soft delete a designation.
        """

        if designation.is_deleted:
            return designation

        designation.delete()

        return designation

    @staticmethod
    @transaction.atomic
    def restore(designation):
        """
        Restore a soft-deleted designation.
        """

        if not designation.is_deleted:
            return designation

        if not designation.organization.is_active:
            raise BusinessRuleException(
                "Cannot restore a designation "
                "belonging to an inactive organization."
            )

        existing_designation = (
            Designation.objects
            .filter(
                organization=designation.organization,
                code=designation.code,
            )
            .exclude(
                pk=designation.pk
            )
            .first()
        )

        if existing_designation:
            raise DuplicateResourceException(
                f"Designation code '{designation.code}' "
                "already exists for this organization."
            )

        designation.restore()

        return designation
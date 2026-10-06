from django.db import transaction
from rest_framework.exceptions import NotFound

from apps.common.exceptions import (
    BusinessRuleException,
    DuplicateResourceException,
)
from apps.departments.models import Department
from apps.organization.models import Organization


class DepartmentService:
    """
    Business operations for Department.
    """

    @staticmethod
    @transaction.atomic
    def create(validated_data):
        """
        Create a new department.
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
                "Cannot create a department for "
                "an inactive organization."
            )

        code = data["code"]

        if Department.objects.filter(
            organization=organization,
            code=code,
        ).exists():
            raise DuplicateResourceException(
                f"Department code '{code}' already "
                f"exists for this organization."
            )

        return Department.objects.create(
            organization=organization,
            **data,
        )

    @staticmethod
    @transaction.atomic
    def update(
        department,
        validated_data,
    ):
        """
        Update an existing department.
        """

        new_code = validated_data.get(
            "code"
        )

        if (
            new_code
            and new_code != department.code
            and Department.objects.filter(
                organization=department.organization,
                code=new_code,
            )
            .exclude(
                pk=department.pk
            )
            .exists()
        ):
            raise DuplicateResourceException(
                f"Department code '{new_code}' "
                "already exists for this organization."
            )

        changed_fields = []

        for field, value in validated_data.items():

            if getattr(
                department,
                field,
            ) != value:

                setattr(
                    department,
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

            department.save(
                update_fields=changed_fields
            )

        return department

    @staticmethod
    @transaction.atomic
    def activate(department):
        """
        Activate a department.
        """

        if department.is_active:
            return department

        if not department.organization.is_active:
            raise BusinessRuleException(
                "Cannot activate a department "
                "belonging to an inactive organization."
            )

        department.is_active = True

        department.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        return department

    @staticmethod
    @transaction.atomic
    def deactivate(department):
        """
        Deactivate a department.
        """

        if not department.is_active:
            return department

        department.is_active = False

        department.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        return department
from django.db import transaction

from apps.common.exceptions import (
    BusinessRuleException,
    DuplicateResourceException,
)

from apps.organization.models import Organization


class OrganizationService:
    """
    Business operations for Organization.
    """

    @staticmethod
    @transaction.atomic
    def create(validated_data):
        """
        Create a new organization.
        """

        code = validated_data["code"]

        if Organization.objects.filter(
            code=code
        ).exists():
            raise DuplicateResourceException(
                f"Organization code '{code}' already exists."
            )

        organization = Organization.objects.create(
            **validated_data
        )

        return organization

    @staticmethod
    @transaction.atomic
    def update(
            organization,
            validated_data,
    ):
        """
        Update an existing organization.
        """

        new_code = validated_data.get(
            "code"
        )

        if (
                new_code
                and new_code != organization.code
                and Organization.objects.filter(
            code=new_code
        )
                .exclude(pk=organization.pk)
                .exists()
        ):
            raise DuplicateResourceException(
                f"Organization code '{new_code}' "
                "already exists."
            )

        changed_fields = []

        for field, value in validated_data.items():

            if getattr(
                    organization,
                    field,
            ) != value:
                setattr(
                    organization,
                    field,
                    value,
                )

                changed_fields.append(field)

        if changed_fields:
            changed_fields.append(
                "updated_at"
            )

            organization.save(
                update_fields=changed_fields
            )

        return organization

    @staticmethod
    @transaction.atomic
    def activate(organization):
        """
        Activate an organization.
        """

        if organization.is_active:
            return organization

        organization.is_active = True

        organization.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        return organization

    @staticmethod
    @transaction.atomic
    def deactivate(organization):
        """
        Deactivate an organization.
        """

        if not organization.is_active:
            return organization

        organization.is_active = False

        organization.save(
            update_fields=[
                "is_active",
                "updated_at",
            ]
        )

        return organization
from rest_framework import serializers

from apps.departments.models import Department


class DepartmentSerializer(
    serializers.ModelSerializer
):
    """
    Serializer used for Department responses.
    """

    organization_uuid = serializers.UUIDField(
        source="organization.uuid",
        read_only=True,
    )

    organization_name = serializers.CharField(
        source="organization.name",
        read_only=True,
    )

    class Meta:
        model = Department

        fields = (
            "uuid",
            "organization_uuid",
            "organization_name",
            "name",
            "code",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "uuid",
            "organization_uuid",
            "organization_name",
            "created_at",
            "updated_at",
        )

class DepartmentCreateSerializer(
    serializers.ModelSerializer
):
    """
    Serializer used when creating a Department.
    """

    organization_uuid = serializers.UUIDField(
        write_only=True,
    )

    class Meta:
        model = Department

        fields = (
            "organization_uuid",
            "name",
            "code",
            "description",
        )

    def validate_organization_uuid(
        self,
        value,
    ):
        from apps.organization.models import (
            Organization,
        )

        try:
            organization = (
                Organization.objects.get(
                    uuid=value
                )
            )
        except Organization.DoesNotExist:
            raise serializers.ValidationError(
                "Organization not found."
            )

        if not organization.is_active:
            raise serializers.ValidationError(
                "Cannot create a department for "
                "an inactive organization."
            )

        return value

    def validate_code(
        self,
        value,
    ):
        return value.strip().upper()

    def validate_name(
        self,
        value,
    ):
        return value.strip()

    def validate_description(
        self,
        value,
    ):
        return value.strip()

class DepartmentUpdateSerializer(
    serializers.ModelSerializer
):
    """
    Serializer used when updating a Department.
    """

    class Meta:
        model = Department

        fields = (
            "name",
            "code",
            "description",
        )

    def validate_code(
        self,
        value,
    ):
        return value.strip().upper()

    def validate_name(
        self,
        value,
    ):
        return value.strip()

    def validate_description(
        self,
        value,
    ):
        return value.strip()
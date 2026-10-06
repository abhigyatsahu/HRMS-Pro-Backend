from rest_framework import serializers

from apps.designations.models import Designation
from apps.organization.models import Organization


class DesignationSerializer(
    serializers.ModelSerializer
):
    """
    Serializer used for Designation responses.
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
        model = Designation

        fields = (
            "uuid",
            "organization_uuid",
            "organization_name",
            "name",
            "code",
            "description",
            "level",
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


class DesignationCreateSerializer(
    serializers.ModelSerializer
):
    """
    Serializer used when creating a Designation.
    """

    organization_uuid = serializers.UUIDField(
        write_only=True,
    )

    class Meta:
        model = Designation

        fields = (
            "organization_uuid",
            "name",
            "code",
            "description",
            "level",
        )

    def validate_organization_uuid(
        self,
        value,
    ):
        try:
            organization = Organization.objects.get(
                uuid=value
            )
        except Organization.DoesNotExist:
            raise serializers.ValidationError(
                "Organization not found."
            )

        if not organization.is_active:
            raise serializers.ValidationError(
                "Cannot create a designation for "
                "an inactive organization."
            )

        return value

    def validate_name(
        self,
        value,
    ):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Designation name cannot be empty."
            )

        return value

    def validate_code(
        self,
        value,
    ):
        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError(
                "Designation code cannot be empty."
            )

        return value

    def validate_level(
        self,
        value,
    ):
        if value < 1:
            raise serializers.ValidationError(
                "Designation level must be greater than or equal to 1."
            )

        return value


class DesignationUpdateSerializer(
    serializers.ModelSerializer
):
    """
    Serializer used when updating a Designation.
    """

    class Meta:
        model = Designation

        fields = (
            "name",
            "code",
            "description",
            "level",
        )

    def validate_name(
        self,
        value,
    ):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Designation name cannot be empty."
            )

        return value

    def validate_code(
        self,
        value,
    ):
        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError(
                "Designation code cannot be empty."
            )

        return value

    def validate_level(
        self,
        value,
    ):
        if value < 1:
            raise serializers.ValidationError(
                "Designation level must be greater than or equal to 1."
            )

        return value
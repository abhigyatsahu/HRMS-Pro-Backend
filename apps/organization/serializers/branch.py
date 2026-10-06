from rest_framework import serializers

from apps.organization.models import Branch


class BranchSerializer(serializers.ModelSerializer):
    """
    Serializer used for Branch responses.
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
        model = Branch

        fields = (
            "uuid",
            "organization_uuid",
            "organization_name",
            "name",
            "code",
            "address",
            "city",
            "state",
            "country",
            "postal_code",
            "phone",
            "email",
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

class BranchCreateSerializer(
    serializers.ModelSerializer
):
    """
    Serializer used when creating a Branch.
    """

    organization_uuid = serializers.UUIDField(
        write_only=True,
    )

    class Meta:
        model = Branch

        fields = (
            "organization_uuid",
            "name",
            "code",
            "address",
            "city",
            "state",
            "country",
            "postal_code",
            "phone",
            "email",
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
                "Cannot create a branch for "
                "an inactive organization."
            )

        return value

    def validate_code(self, value):
        return value.strip().upper()

    def validate_name(self, value):
        return value.strip()

class BranchUpdateSerializer(
    serializers.ModelSerializer
):
    """
    Serializer used when updating a Branch.
    """

    class Meta:
        model = Branch

        fields = (
            "name",
            "code",
            "address",
            "city",
            "state",
            "country",
            "postal_code",
            "phone",
            "email",
        )

    def validate_code(self, value):
        return value.strip().upper()

    def validate_name(self, value):
        return value.strip()
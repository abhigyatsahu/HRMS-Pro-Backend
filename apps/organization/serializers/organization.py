from rest_framework import serializers

from apps.common.constants import (
    FileExtension,
    FileSize,
    ImageDimension,
    MimeType,
)
from apps.common.utils import normalize_spaces
from apps.common.validators import (
    validate_email_address,
    validate_image,
    validate_phone_number,
)

from apps.organization.models import Organization


class OrganizationSerializer(
    serializers.ModelSerializer
):
    """
    Serializer used for reading Organization data.
    """

    class Meta:
        model = Organization

        fields = (
            "uuid",
            "name",
            "code",
            "legal_name",
            "email",
            "phone",
            "website",
            "address",
            "city",
            "state",
            "country",
            "postal_code",
            "logo",
            "is_active",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "uuid",
            "created_at",
            "updated_at",
        )


class OrganizationCreateSerializer(
    serializers.ModelSerializer
):
    """
    Serializer used to create an Organization.
    """

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
    )

    phone = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    class Meta:
        model = Organization

        fields = (
            "name",
            "code",
            "legal_name",
            "email",
            "phone",
            "website",
            "address",
            "city",
            "state",
            "country",
            "postal_code",
            "logo",
        )

    def validate_name(self, value):
        return normalize_spaces(value)

    def validate_code(self, value):
        return value.strip().upper()

    def validate_legal_name(self, value):
        return normalize_spaces(value)

    def validate_email(self, value):
        if not value:
            return value

        return validate_email_address(value)

    def validate_phone(self, value):
        if not value:
            return value

        return validate_phone_number(value)

    def validate_logo(self, value):
        if not value:
            return value

        return validate_image(
            value,
            allowed_extensions=FileExtension.IMAGE,
            allowed_mime_types=MimeType.IMAGE,
            max_size=FileSize.MAX_IMAGE_SIZE,
            min_width=ImageDimension.MIN_WIDTH,
            min_height=ImageDimension.MIN_HEIGHT,
            max_width=ImageDimension.MAX_WIDTH,
            max_height=ImageDimension.MAX_HEIGHT,
        )


class OrganizationUpdateSerializer(
    serializers.ModelSerializer
):
    """
    Serializer used to update an Organization.
    """

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
    )

    phone = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    class Meta:
        model = Organization

        fields = (
            "name",
            "code",
            "legal_name",
            "email",
            "phone",
            "website",
            "address",
            "city",
            "state",
            "country",
            "postal_code",
            "logo",
            "is_active",
        )

    def validate_name(self, value):
        return normalize_spaces(value)

    def validate_code(self, value):
        return value.strip().upper()

    def validate_legal_name(self, value):
        return normalize_spaces(value)

    def validate_email(self, value):
        if not value:
            return value

        return validate_email_address(value)

    def validate_phone(self, value):
        if not value:
            return value

        return validate_phone_number(value)

    def validate_logo(self, value):
        if not value:
            return value

        return validate_image(
            value,
            allowed_extensions=FileExtension.IMAGE,
            allowed_mime_types=MimeType.IMAGE,
            max_size=FileSize.MAX_IMAGE_SIZE,
            min_width=ImageDimension.MIN_WIDTH,
            min_height=ImageDimension.MIN_HEIGHT,
            max_width=ImageDimension.MAX_WIDTH,
            max_height=ImageDimension.MAX_HEIGHT,
        )
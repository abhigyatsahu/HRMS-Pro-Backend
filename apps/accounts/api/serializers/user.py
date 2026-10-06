# api/serializers/user.py

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from ...models import User


class CurrentUserSerializer(
    serializers.ModelSerializer
):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User

        fields = (
            "uuid",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "role",
            "is_staff",
            "is_superuser",
        )
        read_only_fields = fields

    @extend_schema_field(serializers.CharField())
    def get_full_name(self, obj):
        return obj.get_full_name()
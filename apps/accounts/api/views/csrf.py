from django.middleware.csrf import get_token

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, inline_serializer


class CSRFTokenView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(
        operation_id="csrf_token",
        responses={
            200: inline_serializer(
                name="CSRFTokenResponse",
                fields={
                    "success": serializers.BooleanField(default=True),
                    "csrfToken": serializers.CharField(),
                },
            )
        },
        summary="Retrieve CSRF Token",
        description="Retrieve a new CSRF token to include in the headers of subsequent write requests.",
    )
    def get(self, request):
        csrf_token = get_token(request)

        return Response(
            {
                "success": True,
                "csrfToken": csrf_token,
            }
        )
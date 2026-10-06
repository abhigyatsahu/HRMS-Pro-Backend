from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, inline_serializer

from rest_framework_simplejwt.tokens import RefreshToken

from ..serializers.auth import LoginSerializer
from ...services.auth_service import (
    set_access_cookie,
    set_refresh_cookie,
)
import logging
logger = logging.getLogger("hrms.accounts")

class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: inline_serializer(
                name="LoginSuccessResponse",
                fields={
                    "success": serializers.BooleanField(default=True),
                    "message": serializers.CharField(default="Login successful."),
                },
            )
        },
        summary="User Login",
        description="Authenticate a user using credentials. Sets access and refresh tokens in secure cookies.",
    )
    def post(self, request):
        logger.debug("Processing authentication")
        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        response = Response(
            {
                "success": True,
                "message": "Login successful.",
            }
        )


        set_access_cookie(
            response,
            refresh.access_token,
        )

        set_refresh_cookie(
            response,
            refresh,
        )
        logger.info(
            "User authenticated successfully"
        )
        return response
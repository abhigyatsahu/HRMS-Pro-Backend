from django.conf import settings

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, inline_serializer

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from ...services.auth_service import clear_auth_cookies
import logging

logger = logging.getLogger("hrms.accounts")


class LogoutView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(
        request=None,
        responses={
            200: inline_serializer(
                name="LogoutResponse",
                fields={
                    "success": serializers.BooleanField(default=True),
                    "message": serializers.CharField(default="Logged out successfully."),
                },
            )
        },
        summary="Logout User",
        description="Clear access and refresh tokens from HTTP-only cookies and blacklist the refresh token.",
    )
    def post(self, request):
        logger.debug("Processing logout")
        refresh_token = request.COOKIES.get(
            settings.JWT_REFRESH_COOKIE
        )

        if refresh_token:
            try:
                RefreshToken(
                    refresh_token
                ).blacklist()

            except TokenError:
                pass

        response = Response(
            {
                "success": True,
                "message": "Logged out successfully.",
            },
            status=status.HTTP_200_OK,
        )

        clear_auth_cookies(response)
        logger.info(f"User logged out successfully")
        return response
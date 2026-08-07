from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from ...services.auth_service import (
    clear_auth_cookies,
    set_access_cookie,
    set_refresh_cookie,
)
import logging

logger = logging.getLogger("hrms.accounts")

User = get_user_model()


class RefreshTokenView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        logger.debug("Trying Session Refresh")
        token = request.COOKIES.get(
            settings.JWT_REFRESH_COOKIE
        )

        if not token:
            return Response(
                {
                    "success": False,
                    "message": "Refresh token not found.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            old_refresh = RefreshToken(token)

            user_id = old_refresh[
                settings.SIMPLE_JWT["USER_ID_CLAIM"]
            ]

            user = User.objects.get(
                **{
                    settings.SIMPLE_JWT["USER_ID_FIELD"]:
                        user_id
                }
            )

            if not user.is_active:
                raise TokenError(
                    "User account is inactive."
                )

            old_refresh.blacklist()

            new_refresh = RefreshToken.for_user(user)

            response = Response(
                {
                    "success": True,
                    "message": "Session refreshed successfully.",
                },
                status=status.HTTP_200_OK,
            )

            set_access_cookie(
                response,
                new_refresh.access_token,
            )

            set_refresh_cookie(
                response,
                new_refresh,
            )

            logger.info("Authentication session refreshed.")

            return response

        except (
            TokenError,
            User.DoesNotExist,
        ):
            logger.warning("Invalid refresh token received.")
            response = Response(
                {
                    "success": False,
                    "message": "Invalid or expired session.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

            clear_auth_cookies(response)

            return response
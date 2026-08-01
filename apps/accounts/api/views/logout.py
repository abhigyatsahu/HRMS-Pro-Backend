from django.conf import settings

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from ...services.auth_service import clear_auth_cookies
import logging

logger = logging.getLogger("hrms.accounts")


class LogoutView(APIView):
    permission_classes = [AllowAny]

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
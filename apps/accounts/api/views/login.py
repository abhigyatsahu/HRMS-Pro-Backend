# api/views/login.py

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

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
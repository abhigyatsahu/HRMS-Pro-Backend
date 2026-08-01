# api/views/me.py
import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.user import CurrentUserSerializer

logger = logging.getLogger("hrms.accounts")

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.debug("Getting current user")
        serializer = CurrentUserSerializer(
            request.user
        )
        logger.info("Current user is {}".format(request.user.username))
        return Response(
            {
                "success": True,
                "message": "Current user retrieved successfully.",
                "data": serializer.data,
            }
        )
# api/views/me.py
import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, inline_serializer

from ..serializers.user import CurrentUserSerializer

logger = logging.getLogger("hrms.accounts")

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={
            200: inline_serializer(
                name="CurrentUserResponse",
                fields={
                    "success": serializers.BooleanField(default=True),
                    "message": serializers.CharField(default="Current user retrieved successfully."),
                    "data": CurrentUserSerializer(),
                },
            )
        },
        summary="Retrieve Current User",
        description="Get the authenticated user's profile details.",
    )
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
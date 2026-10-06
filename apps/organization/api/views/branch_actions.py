from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, inline_serializer

from apps.common.permissions import (
    OrganizationStatusPermission,
)
from apps.common.utils import success_payload
from apps.organization.models import Branch
from apps.organization.serializers import (
    BranchSerializer,
)
from apps.organization.services import BranchService


class BranchActivateView(APIView):
    """
    Activate a branch.
    """

    permission_classes = [
        OrganizationStatusPermission,
    ]

    @extend_schema(
        request=None,
        responses={
            200: inline_serializer(
                name="BranchActivateSuccessResponse",
                fields={
                    "success": serializers.BooleanField(default=True),
                    "message": serializers.CharField(default="Branch activated successfully."),
                    "data": BranchSerializer(),
                },
            )
        },
        summary="Activate Branch",
        description="Activate a branch by its UUID.",
    )
    def post(
        self,
        request,
        uuid,
    ):
        branch = get_object_or_404(
            Branch.objects.select_related(
                "organization"
            ),
            uuid=uuid,
        )

        branch = BranchService.activate(
            branch
        )

        serializer = BranchSerializer(
            branch
        )

        return Response(
            success_payload(
                message=(
                    "Branch activated successfully."
                ),
                data=serializer.data,
            ),
            status=status.HTTP_200_OK,
        )


class BranchDeactivateView(APIView):
    """
    Deactivate a branch.
    """

    permission_classes = [
        OrganizationStatusPermission,
    ]

    @extend_schema(
        request=None,
        responses={
            200: inline_serializer(
                name="BranchDeactivateSuccessResponse",
                fields={
                    "success": serializers.BooleanField(default=True),
                    "message": serializers.CharField(default="Branch deactivated successfully."),
                    "data": BranchSerializer(),
                },
            )
        },
        summary="Deactivate Branch",
        description="Deactivate a branch by its UUID.",
    )
    def post(
        self,
        request,
        uuid,
    ):
        branch = get_object_or_404(
            Branch.objects.select_related(
                "organization"
            ),
            uuid=uuid,
        )

        branch = BranchService.deactivate(
            branch
        )

        serializer = BranchSerializer(
            branch
        )

        return Response(
            success_payload(
                message=(
                    "Branch deactivated successfully."
                ),
                data=serializer.data,
            ),
            status=status.HTTP_200_OK,
        )
from django.shortcuts import get_object_or_404

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import (
    extend_schema,
    inline_serializer,
)

from apps.common.permissions import (
    DesignationDeletePermission,
    DesignationStatusPermission,
)
from apps.common.utils import success_payload

from apps.designations.models import Designation
from apps.designations.serializers import (
    DesignationSerializer,
)
from apps.designations.services import (
    DesignationService,
)


class DesignationActivateView(APIView):
    """
    Activate a designation.
    """

    permission_classes = [
        DesignationStatusPermission,
    ]

    @extend_schema(
        request=None,
        responses={
            200: inline_serializer(
                name="DesignationActivateSuccessResponse",
                fields={
                    "success": serializers.BooleanField(
                        default=True
                    ),
                    "message": serializers.CharField(
                        default=(
                            "Designation activated successfully."
                        )
                    ),
                    "data": DesignationSerializer(),
                },
            )
        },
        summary="Activate Designation",
        description=(
            "Activate a designation by its UUID."
        ),
    )
    def post(
        self,
        request,
        uuid,
    ):
        designation = get_object_or_404(
            Designation.objects.select_related(
                "organization"
            ),
            uuid=uuid,
        )

        designation = DesignationService.activate(
            designation
        )

        serializer = DesignationSerializer(
            designation
        )

        return Response(
            success_payload(
                message=(
                    "Designation activated successfully."
                ),
                data=serializer.data,
            ),
            status=status.HTTP_200_OK,
        )


class DesignationDeactivateView(APIView):
    """
    Deactivate a designation.
    """

    permission_classes = [
        DesignationStatusPermission,
    ]

    @extend_schema(
        request=None,
        responses={
            200: inline_serializer(
                name="DesignationDeactivateSuccessResponse",
                fields={
                    "success": serializers.BooleanField(
                        default=True
                    ),
                    "message": serializers.CharField(
                        default=(
                            "Designation deactivated successfully."
                        )
                    ),
                    "data": DesignationSerializer(),
                },
            )
        },
        summary="Deactivate Designation",
        description=(
            "Deactivate a designation by its UUID."
        ),
    )
    def post(
        self,
        request,
        uuid,
    ):
        designation = get_object_or_404(
            Designation.objects.select_related(
                "organization"
            ),
            uuid=uuid,
        )

        designation = DesignationService.deactivate(
            designation
        )

        serializer = DesignationSerializer(
            designation
        )

        return Response(
            success_payload(
                message=(
                    "Designation deactivated successfully."
                ),
                data=serializer.data,
            ),
            status=status.HTTP_200_OK,
        )


class DesignationDeleteView(APIView):
    """
    Soft delete a designation.
    """

    permission_classes = [
        DesignationDeletePermission,
    ]

    @extend_schema(
        request=None,
        responses={
            200: inline_serializer(
                name="DesignationDeleteSuccessResponse",
                fields={
                    "success": serializers.BooleanField(
                        default=True
                    ),
                    "message": serializers.CharField(
                        default=(
                            "Designation deleted successfully."
                        )
                    ),
                },
            )
        },
        summary="Delete Designation",
        description=(
            "Soft delete a designation by its UUID."
        ),
    )
    def delete(
        self,
        request,
        uuid,
    ):
        designation = get_object_or_404(
            Designation.objects.select_related(
                "organization"
            ),
            uuid=uuid,
        )

        DesignationService.delete(
            designation
        )

        return Response(
            success_payload(
                message=(
                    "Designation deleted successfully."
                ),
                data=None,
            ),
            status=status.HTTP_200_OK,
        )

class DesignationRestoreView(APIView):
    """
    Restore a soft-deleted designation.
    """

    permission_classes = [
        DesignationDeletePermission,
    ]

    @extend_schema(
        request=None,
        responses={
            200: inline_serializer(
                name="DesignationRestoreSuccessResponse",
                fields={
                    "success": serializers.BooleanField(
                        default=True
                    ),
                    "message": serializers.CharField(
                        default=(
                            "Designation restored successfully."
                        )
                    ),
                    "data": DesignationSerializer(),
                },
            )
        },
        summary="Restore Designation",
        description=(
            "Restore a soft-deleted designation by its UUID."
        ),
    )
    def post(
        self,
        request,
        uuid,
    ):
        designation = get_object_or_404(
            Designation.all_objects.select_related(
                "organization"
            ),
            uuid=uuid,
        )

        designation = DesignationService.restore(
            designation
        )

        serializer = DesignationSerializer(
            designation
        )

        return Response(
            success_payload(
                message=(
                    "Designation restored successfully."
                ),
                data=serializer.data,
            ),
            status=status.HTTP_200_OK,
        )
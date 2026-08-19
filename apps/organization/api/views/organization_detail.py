from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.utils import success_payload
from apps.organization.models import Organization
from apps.organization.serializers import (
    OrganizationSerializer,
    OrganizationUpdateSerializer,
)
from apps.organization.services import (
    OrganizationService,
)
from apps.common.permissions import (
    OrganizationManagePermission,
    OrganizationReadPermission,
)

class OrganizationDetailView(
    generics.RetrieveUpdateAPIView
):
    """
    Retrieve and update an organization.
    """

    queryset = Organization.objects.all()

    lookup_field = "uuid"

    def get_permissions(self):
        if self.request.method == "GET":
            permission_class = (
                OrganizationReadPermission
            )
        else:
            permission_class = (
                OrganizationManagePermission
            )

        return [
            permission_class()
        ]

    def get_serializer_class(self):
        if self.request.method in (
            "PUT",
            "PATCH",
        ):
            return OrganizationUpdateSerializer

        return OrganizationSerializer

    def retrieve(
        self,
        request,
        *args,
        **kwargs,
    ):
        organization = self.get_object()

        serializer = OrganizationSerializer(
            organization
        )

        return Response(
            success_payload(
                message=(
                    "Organization retrieved successfully."
                ),
                data=serializer.data,
            ),
            status=status.HTTP_200_OK,
        )

    def update(
        self,
        request,
        *args,
        **kwargs,
    ):
        partial = kwargs.pop(
            "partial",
            False,
        )

        organization = self.get_object()

        serializer = self.get_serializer(
            organization,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(
            raise_exception=True
        )

        organization = OrganizationService.update(
            organization,
            serializer.validated_data,
        )

        response_serializer = OrganizationSerializer(
            organization
        )

        return Response(
            success_payload(
                message=(
                    "Organization updated successfully."
                ),
                data=response_serializer.data,
            ),
            status=status.HTTP_200_OK,
        )
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils import success_payload
from apps.organization.models import Organization
from apps.organization.serializers import (
    OrganizationSerializer,
)
from apps.organization.services import (
    OrganizationService,
)
from apps.common.permissions import (
    OrganizationStatusPermission,
)

class OrganizationActivateView(APIView):
    """
    Activate an organization.
    """

    permission_classes = [
        OrganizationStatusPermission,
    ]

    def post(self, request, uuid):
        organization = get_object_or_404(
            Organization,
            uuid=uuid,
        )

        organization = OrganizationService.activate(
            organization
        )

        serializer = OrganizationSerializer(
            organization
        )

        return Response(
            success_payload(
                message=(
                    "Organization activated successfully."
                ),
                data=serializer.data,
            ),
            status=status.HTTP_200_OK,
        )


class OrganizationDeactivateView(APIView):
    """
    Deactivate an organization.
    """

    permission_classes = [
        OrganizationStatusPermission,
    ]

    def post(self, request, uuid):
        organization = get_object_or_404(
            Organization,
            uuid=uuid,
        )

        organization = OrganizationService.deactivate(
            organization
        )

        serializer = OrganizationSerializer(
            organization
        )

        return Response(
            success_payload(
                message=(
                    "Organization deactivated successfully."
                ),
                data=serializer.data,
            ),
            status=status.HTTP_200_OK,
        )
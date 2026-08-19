from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.common.utils import success_payload
from apps.organization.models import Organization
from apps.organization.serializers import (
    OrganizationCreateSerializer,
    OrganizationSerializer,
)
from apps.organization.services import (
    OrganizationService,
)
from apps.common.permissions import (
    OrganizationManagePermission,
    OrganizationReadPermission,
)


class OrganizationListCreateView(
    generics.ListCreateAPIView
):
    """
    List and create organizations.
    """


    queryset = Organization.objects.all()

    search_fields = (
        "name",
        "code",
        "legal_name",
        "email",
        "phone",
    )

    ordering_fields = (
        "name",
        "code",
        "created_at",
        "updated_at",
    )

    ordering = (
        "name",
    )

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
        if self.request.method == "POST":
            return OrganizationCreateSerializer

        return OrganizationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        organization = OrganizationService.create(
            serializer.validated_data
        )

        response_serializer = OrganizationSerializer(
            organization
        )

        return Response(
            success_payload(
                message=(
                    "Organization created successfully."
                ),
                data=response_serializer.data,
            ),
            status=status.HTTP_201_CREATED,
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset()
        )

        page = self.paginate_queryset(
            queryset
        )

        if page is not None:
            serializer = self.get_serializer(
                page,
                many=True,
            )

            return self.get_paginated_response(
                serializer.data
            )

        serializer = self.get_serializer(
            queryset,
            many=True,
        )

        return Response(
            success_payload(
                message=(
                    "Organizations retrieved successfully."
                ),
                data=serializer.data,
            ),
            status=status.HTTP_200_OK,
        )


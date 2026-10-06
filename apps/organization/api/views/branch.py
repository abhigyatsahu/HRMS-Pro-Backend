from rest_framework import generics, status
from rest_framework.response import Response

from apps.common.permissions import (
    OrganizationManagePermission,
    OrganizationReadPermission,
)
from apps.common.utils import success_payload
from apps.organization.models import Branch
from apps.organization.serializers import (
    BranchCreateSerializer,
    BranchSerializer,
    BranchUpdateSerializer,
)
from apps.organization.services import BranchService


class BranchListCreateView(
    generics.ListCreateAPIView
):
    """
    List and create branches.
    """

    queryset = (
        Branch.objects
        .select_related("organization")
        .all()
    )

    search_fields = (
        "name",
        "code",
        "city",
        "state",
        "email",
        "phone",
        "organization__name",
        "organization__code",
    )

    ordering_fields = (
        "name",
        "code",
        "city",
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
            return BranchCreateSerializer

        return BranchSerializer

    def list(
        self,
        request,
        *args,
        **kwargs,
    ):
        queryset = self.filter_queryset(
            self.get_queryset()
        )

        page = self.paginate_queryset(
            queryset
        )

        if page is not None:
            serializer = BranchSerializer(
                page,
                many=True,
            )

            return self.get_paginated_response(
                serializer.data
            )

        serializer = BranchSerializer(
            queryset,
            many=True,
        )

        return Response(
            success_payload(
                message=(
                    "Branches retrieved successfully."
                ),
                data=serializer.data,
            ),
            status=status.HTTP_200_OK,
        )

    def create(
        self,
        request,
        *args,
        **kwargs,
    ):
        serializer = self.get_serializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        branch = BranchService.create(
            serializer.validated_data
        )

        response_serializer = BranchSerializer(
            branch
        )

        return Response(
            success_payload(
                message=(
                    "Branch created successfully."
                ),
                data=response_serializer.data,
            ),
            status=status.HTTP_201_CREATED,
        )

class BranchDetailView(
    generics.RetrieveUpdateAPIView
):
    """
    Retrieve and update a branch.
    """

    queryset = (
        Branch.objects
        .select_related("organization")
        .all()
    )

    lookup_field = "uuid"

    def get_permissions(self):
        return [
            (
                OrganizationReadPermission
                if self.request.method == "GET"
                else OrganizationManagePermission
            )()
        ]

    def get_serializer_class(self):
        if self.request.method in (
            "PUT",
            "PATCH",
        ):
            return BranchUpdateSerializer

        return BranchSerializer

    def retrieve(
        self,
        request,
        *args,
        **kwargs,
    ):
        branch = self.get_object()

        serializer = BranchSerializer(
            branch
        )

        return Response(
            success_payload(
                message=(
                    "Branch retrieved successfully."
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

        branch = self.get_object()

        serializer = self.get_serializer(
            branch,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(
            raise_exception=True
        )

        branch = BranchService.update(
            branch,
            serializer.validated_data,
        )

        response_serializer = BranchSerializer(
            branch
        )

        return Response(
            success_payload(
                message=(
                    "Branch updated successfully."
                ),
                data=response_serializer.data,
            ),
            status=status.HTTP_200_OK,
        )
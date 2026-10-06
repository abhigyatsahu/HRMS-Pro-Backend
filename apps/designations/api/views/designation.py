from rest_framework import generics, status
from rest_framework.response import Response

from apps.common.permissions import (
    DesignationManagePermission,
    DesignationReadPermission,
    DesignationDeletePermission,
)
from apps.common.utils import success_payload

from apps.designations.models import Designation
from apps.designations.serializers import (
    DesignationCreateSerializer,
    DesignationSerializer,
    DesignationUpdateSerializer,
)
from apps.designations.services import (
    DesignationService,
)


class DesignationListCreateView(
    generics.ListCreateAPIView
):
    """
    List and create designations.
    """

    queryset = (
        Designation.objects
        .select_related("organization")
        .all()
    )

    search_fields = (
        "name",
        "code",
        "description",
        "organization__name",
        "organization__code",
    )

    ordering_fields = (
        "name",
        "code",
        "level",
        "created_at",
        "updated_at",
    )

    ordering = (
        "level",
        "name",
    )

    def get_permissions(self):
        if self.request.method == "GET":
            permission_class = (
                DesignationReadPermission
            )
        else:
            permission_class = (
                DesignationManagePermission
            )

        return [
            permission_class()
        ]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return DesignationCreateSerializer

        return DesignationSerializer

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
            serializer = DesignationSerializer(
                page,
                many=True,
            )

            return self.get_paginated_response(
                serializer.data
            )

        serializer = DesignationSerializer(
            queryset,
            many=True,
        )

        return Response(
            success_payload(
                message=(
                    "Designations retrieved successfully."
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

        designation = DesignationService.create(
            serializer.validated_data
        )

        response_serializer = DesignationSerializer(
            designation
        )

        return Response(
            success_payload(
                message=(
                    "Designation created successfully."
                ),
                data=response_serializer.data,
            ),
            status=status.HTTP_201_CREATED,
        )


class DesignationDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    """
    Retrieve and update a designation.
    """

    queryset = (
        Designation.objects
        .select_related("organization")
        .all()
    )

    lookup_field = "uuid"

    def get_permissions(self):
        if self.request.method == "GET":
            permission_class = DesignationReadPermission

        elif self.request.method == "DELETE":
            permission_class = DesignationDeletePermission

        else:
            permission_class = DesignationManagePermission

        return [
            permission_class()
        ]

    def get_serializer_class(self):
        if self.request.method in (
            "PUT",
            "PATCH",
        ):
            return DesignationUpdateSerializer

        return DesignationSerializer

    def retrieve(
        self,
        request,
        *args,
        **kwargs,
    ):
        designation = self.get_object()

        serializer = DesignationSerializer(
            designation
        )

        return Response(
            success_payload(
                message=(
                    "Designation retrieved successfully."
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

        designation = self.get_object()

        serializer = self.get_serializer(
            designation,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(
            raise_exception=True
        )

        designation = DesignationService.update(
            designation,
            serializer.validated_data,
        )

        response_serializer = DesignationSerializer(
            designation
        )

        return Response(
            success_payload(
                message=(
                    "Designation updated successfully."
                ),
                data=response_serializer.data,
            ),
            status=status.HTTP_200_OK,
        )

    def destroy(
            self,
            request,
            *args,
            **kwargs,
    ):
        designation = self.get_object()

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
from rest_framework import generics, status
from rest_framework.response import Response

from apps.common.permissions import (
    OrganizationManagePermission,
    OrganizationReadPermission,
    OrganizationStatusPermission,
)
from apps.common.utils import success_payload
from apps.departments.models import Department
from apps.departments.serializers import (
    DepartmentCreateSerializer,
    DepartmentSerializer,
    DepartmentUpdateSerializer,
)
from apps.departments.services import (
    DepartmentService,
)


class DepartmentListCreateView(
    generics.ListCreateAPIView
):
    """
    List and create departments.
    """

    queryset = (
        Department.objects
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
            return DepartmentCreateSerializer

        return DepartmentSerializer

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
            serializer = DepartmentSerializer(
                page,
                many=True,
            )

            return self.get_paginated_response(
                serializer.data
            )

        serializer = DepartmentSerializer(
            queryset,
            many=True,
        )

        return Response(
            success_payload(
                message=(
                    "Departments retrieved "
                    "successfully."
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

        department = DepartmentService.create(
            serializer.validated_data
        )

        response_serializer = (
            DepartmentSerializer(
                department
            )
        )

        return Response(
            success_payload(
                message=(
                    "Department created "
                    "successfully."
                ),
                data=response_serializer.data,
            ),
            status=status.HTTP_201_CREATED,
        )

class DepartmentDetailView(
    generics.RetrieveUpdateAPIView
):
    """
    Retrieve and update a department.
    """

    queryset = (
        Department.objects
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
            return DepartmentUpdateSerializer

        return DepartmentSerializer

    def retrieve(
        self,
        request,
        *args,
        **kwargs,
    ):
        department = self.get_object()

        serializer = DepartmentSerializer(
            department
        )

        return Response(
            success_payload(
                message=(
                    "Department retrieved "
                    "successfully."
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

        department = self.get_object()

        serializer = self.get_serializer(
            department,
            data=request.data,
            partial=partial,
        )

        serializer.is_valid(
            raise_exception=True
        )

        department = DepartmentService.update(
            department,
            serializer.validated_data,
        )

        response_serializer = (
            DepartmentSerializer(
                department
            )
        )

        return Response(
            success_payload(
                message=(
                    "Department updated "
                    "successfully."
                ),
                data=response_serializer.data,
            ),
            status=status.HTTP_200_OK,
        )

class DepartmentActivateView(
    generics.GenericAPIView
):
    """
    Activate a department.
    """

    queryset = (
        Department.objects
        .select_related("organization")
        .all()
    )

    lookup_field = "uuid"

    serializer_class = DepartmentSerializer

    permission_classes = (
        OrganizationStatusPermission,
    )

    def post(
        self,
        request,
        *args,
        **kwargs,
    ):
        department = self.get_object()

        department = (
            DepartmentService.activate(
                department
            )
        )

        serializer = DepartmentSerializer(
            department
        )

        return Response(
            success_payload(
                message=(
                    "Department activated "
                    "successfully."
                ),
                data=serializer.data,
            ),
            status=status.HTTP_200_OK,
        )


class DepartmentDeactivateView(
    generics.GenericAPIView
):
    """
    Deactivate a department.
    """

    queryset = (
        Department.objects
        .select_related("organization")
        .all()
    )

    lookup_field = "uuid"

    serializer_class = DepartmentSerializer

    permission_classes = (
        OrganizationStatusPermission,
    )

    def post(
        self,
        request,
        *args,
        **kwargs,
    ):
        department = self.get_object()

        department = (
            DepartmentService.deactivate(
                department
            )
        )

        serializer = DepartmentSerializer(
            department
        )

        return Response(
            success_payload(
                message=(
                    "Department deactivated "
                    "successfully."
                ),
                data=serializer.data,
            ),
            status=status.HTTP_200_OK,
        )
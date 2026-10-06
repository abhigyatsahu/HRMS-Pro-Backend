from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.utils.response import error_payload, success_payload
from apps.core.pagination.pagination import StandardPagination
from apps.employees.models import Employee
from apps.employees.serializers import (
    EmployeeCreateSerializer,
    EmployeeSerializer,
    EmployeeUpdateSerializer,
)
from apps.employees.services import EmployeeService


class EmployeeListCreateView(APIView):
    """
    List and create employees.
    """

    pagination_class = StandardPagination

    def get_queryset(self):
        queryset = (
            Employee.objects
            .select_related(
                "organization",
                "branch",
                "department",
                "designation",
                "reporting_manager",
            )
            .order_by("employee_code")
        )

        request = self.request

        search = request.query_params.get("search")
        if search:
            queryset = queryset.search(search)

        organization = request.query_params.get(
            "organization"
        )
        if organization:
            queryset = queryset.filter(
                organization__uuid=organization
            )

        branch = request.query_params.get("branch")
        if branch:
            queryset = queryset.filter(
                branch__uuid=branch
            )

        department = request.query_params.get(
            "department"
        )
        if department:
            queryset = queryset.filter(
                department__uuid=department
            )

        designation = request.query_params.get(
            "designation"
        )
        if designation:
            queryset = queryset.filter(
                designation__uuid=designation
            )

        employment_status = request.query_params.get(
            "employment_status"
        )
        if employment_status:
            queryset = queryset.filter(
                employment_status=employment_status
            )

        employment_type = request.query_params.get(
            "employment_type"
        )
        if employment_type:
            queryset = queryset.filter(
                employment_type=employment_type
            )

        is_active = request.query_params.get(
            "is_active"
        )
        if is_active is not None:
            is_active_value = (
                is_active.lower() == "true"
            )
            queryset = queryset.filter(
                is_active=is_active_value
            )

        return queryset

    def get(self, request):
        queryset = self.get_queryset()

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(
            queryset,
            request,
            view=self,
        )

        serializer = EmployeeSerializer(
            page,
            many=True,
        )

        return paginator.get_paginated_response(
            serializer.data
        )

    def post(self, request):
        serializer = EmployeeCreateSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                error_payload(
                    message="Employee creation failed.",
                    errors=serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        employee = EmployeeService.create_employee(
            validated_data=serializer.validated_data
        )

        response_serializer = EmployeeSerializer(
            employee
        )

        return Response(
            success_payload(
                message="Employee created successfully.",
                data=response_serializer.data,
            ),
            status=status.HTTP_201_CREATED,
        )


class EmployeeDetailView(APIView):
    """
    Retrieve, update and soft-delete an employee.
    """

    def get_object(self, uuid):
        try:
            return (
                Employee.objects
                .select_related(
                    "organization",
                    "branch",
                    "department",
                    "designation",
                    "reporting_manager",
                )
                .get(uuid=uuid)
            )
        except Employee.DoesNotExist:
            return None

    def get(self, request, uuid):
        employee = self.get_object(uuid)

        if employee is None:
            return Response(
                error_payload(
                    message="Employee not found."
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = EmployeeSerializer(employee)

        return Response(
            success_payload(
                message="Employee fetched successfully.",
                data=serializer.data,
            ),
            status=status.HTTP_200_OK,
        )

    def put(self, request, uuid):
        employee = self.get_object(uuid)

        if employee is None:
            return Response(
                error_payload(
                    message="Employee not found."
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = EmployeeUpdateSerializer(
            employee,
            data=request.data,
        )

        if not serializer.is_valid():
            return Response(
                error_payload(
                    message="Employee update failed.",
                    errors=serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        employee = EmployeeService.update_employee(
            employee=employee,
            validated_data=serializer.validated_data,
        )

        response_serializer = EmployeeSerializer(
            employee
        )

        return Response(
            success_payload(
                message="Employee updated successfully.",
                data=response_serializer.data,
            ),
            status=status.HTTP_200_OK,
        )

    def patch(self, request, uuid):
        employee = self.get_object(uuid)

        if employee is None:
            return Response(
                error_payload(
                    message="Employee not found."
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = EmployeeUpdateSerializer(
            employee,
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():
            return Response(
                error_payload(
                    message="Employee update failed.",
                    errors=serializer.errors,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        employee = EmployeeService.update_employee(
            employee=employee,
            validated_data=serializer.validated_data,
        )

        response_serializer = EmployeeSerializer(
            employee
        )

        return Response(
            success_payload(
                message="Employee updated successfully.",
                data=response_serializer.data,
            ),
            status=status.HTTP_200_OK,
        )

    def delete(self, request, uuid):
        employee = self.get_object(uuid)

        if employee is None:
            return Response(
                error_payload(
                    message="Employee not found."
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        EmployeeService.delete_employee(
            employee=employee
        )

        return Response(
            success_payload(
                message="Employee deleted successfully.",
                data=None,
            ),
            status=status.HTTP_200_OK,
        )


class EmployeeRestoreView(APIView):
    """
    Restore a soft-deleted employee.
    """

    def post(self, request, uuid):
        try:
            employee = Employee.all_objects.get(
                uuid=uuid
            )
        except Employee.DoesNotExist:
            return Response(
                error_payload(
                    message="Employee not found."
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        if not employee.is_deleted:
            return Response(
                error_payload(
                    message="Employee is not deleted."
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        employee = EmployeeService.restore_employee(
            employee=employee
        )

        serializer = EmployeeSerializer(employee)

        return Response(
            success_payload(
                message="Employee restored successfully.",
                data=serializer.data,
            ),
            status=status.HTTP_200_OK,
        )


class EmployeeActivateView(APIView):
    """
    Activate an employee.
    """

    def post(self, request, uuid):
        try:
            employee = Employee.objects.get(
                uuid=uuid
            )
        except Employee.DoesNotExist:
            return Response(
                error_payload(
                    message="Employee not found."
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        if employee.is_active:
            return Response(
                error_payload(
                    message="Employee is already active."
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        employee = EmployeeService.activate_employee(
            employee=employee
        )

        serializer = EmployeeSerializer(employee)

        return Response(
            success_payload(
                message="Employee activated successfully.",
                data=serializer.data,
            ),
            status=status.HTTP_200_OK,
        )


class EmployeeDeactivateView(APIView):
    """
    Deactivate an employee.
    """

    def post(self, request, uuid):
        try:
            employee = Employee.objects.get(
                uuid=uuid
            )
        except Employee.DoesNotExist:
            return Response(
                error_payload(
                    message="Employee not found."
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        if not employee.is_active:
            return Response(
                error_payload(
                    message="Employee is already inactive."
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        employee = EmployeeService.deactivate_employee(
            employee=employee
        )

        serializer = EmployeeSerializer(employee)

        return Response(
            success_payload(
                message="Employee deactivated successfully.",
                data=serializer.data,
            ),
            status=status.HTTP_200_OK,
        )
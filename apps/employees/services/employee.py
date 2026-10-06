from django.db import transaction

from apps.employees.models import Employee


class EmployeeService:

    @staticmethod
    @transaction.atomic
    def create_employee(*, validated_data):
        """
        Create a new employee.
        """

        employee = Employee.objects.create(
            **validated_data
        )

        return employee

    @staticmethod
    @transaction.atomic
    def update_employee(
        *,
        employee,
        validated_data,
    ):
        """
        Update an existing employee.
        """

        for field, value in validated_data.items():
            setattr(
                employee,
                field,
                value,
            )

        employee.save()

        return employee

    @staticmethod
    @transaction.atomic
    def delete_employee(*, employee):
        """
        Soft delete an employee.
        """

        employee.delete()

        return employee

    @staticmethod
    @transaction.atomic
    def restore_employee(*, employee):
        """
        Restore a soft-deleted employee.
        """

        employee.restore()

        return employee

    @staticmethod
    @transaction.atomic
    def activate_employee(*, employee):
        """
        Activate an employee.
        """

        employee.is_active = True
        employee.employment_status = "ACTIVE"
        employee.save(
            update_fields=[
                "is_active",
                "employment_status",
                "updated_at",
            ]
        )

        return employee

    @staticmethod
    @transaction.atomic
    def deactivate_employee(*, employee):
        """
        Deactivate an employee.
        """

        employee.is_active = False
        employee.employment_status = "INACTIVE"
        employee.save(
            update_fields=[
                "is_active",
                "employment_status",
                "updated_at",
            ]
        )

        return employee
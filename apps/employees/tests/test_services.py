from django.test import TestCase

from apps.employees.services import EmployeeService
from apps.employees.tests.factories import (
    create_branch,
    create_department,
    create_designation,
    create_employee,
    create_organization,
)


class EmployeeServiceTestCase(TestCase):

    def setUp(self):
        self.organization = create_organization(
            code="SRV-ORG",
            name="Service Organization",
        )

        self.branch = create_branch(
            organization=self.organization,
            code="SRV-BR",
            name="Service Branch",
        )

        self.department = create_department(
            organization=self.organization,
            code="SRV-DEP",
            name="Service Department",
        )

        self.designation = create_designation(
            organization=self.organization,
            code="SRV-DES",
            name="Service Designation",
        )

    def test_create_employee(self):
        employee = EmployeeService.create_employee(
            validated_data={
                "employee_code": "SRV001",
                "first_name": "Service",
                "middle_name": "",
                "last_name": "Employee",
                "organization": self.organization,
                "branch": self.branch,
                "department": self.department,
                "designation": self.designation,
                "joining_date": "2026-01-01",
                "employment_type": "FULL TIME",
                "employment_status": "ACTIVE",
                "is_active": True,
            }
        )

        self.assertIsNotNone(employee.pk)
        self.assertEqual(
            employee.employee_code,
            "SRV001",
        )
        self.assertEqual(
            employee.organization,
            self.organization,
        )

    def test_update_employee(self):
        employee = create_employee(
            organization=self.organization,
            branch=self.branch,
            department=self.department,
            designation=self.designation,
            employee_code="SRV002",
            first_name="Old",
        )

        updated_employee = EmployeeService.update_employee(
            employee=employee,
            validated_data={
                "first_name": "Updated",
                "last_name": "Name",
            },
        )

        updated_employee.refresh_from_db()

        self.assertEqual(
            updated_employee.first_name,
            "Updated",
        )
        self.assertEqual(
            updated_employee.last_name,
            "Name",
        )

    def test_delete_employee(self):
        employee = create_employee(
            organization=self.organization,
            branch=self.branch,
            department=self.department,
            designation=self.designation,
            employee_code="SRV003",
        )

        EmployeeService.delete_employee(
            employee=employee,
        )

        employee.refresh_from_db()

        self.assertTrue(
            employee.is_deleted
        )
        self.assertIsNotNone(
            employee.deleted_at
        )

    def test_deleted_employee_is_hidden_from_default_manager(self):
        employee = create_employee(
            organization=self.organization,
            branch=self.branch,
            department=self.department,
            designation=self.designation,
            employee_code="SRV004",
        )

        EmployeeService.delete_employee(
            employee=employee,
        )

        self.assertFalse(
            employee.__class__.objects.filter(
                pk=employee.pk
            ).exists()
        )

        self.assertTrue(
            employee.__class__.all_objects.filter(
                pk=employee.pk
            ).exists()
        )

    def test_restore_employee(self):
        employee = create_employee(
            organization=self.organization,
            branch=self.branch,
            department=self.department,
            designation=self.designation,
            employee_code="SRV005",
        )

        EmployeeService.delete_employee(
            employee=employee,
        )

        EmployeeService.restore_employee(
            employee=employee,
        )

        employee.refresh_from_db()

        self.assertFalse(
            employee.is_deleted
        )
        self.assertIsNone(
            employee.deleted_at
        )

    def test_activate_employee(self):
        employee = create_employee(
            organization=self.organization,
            branch=self.branch,
            department=self.department,
            designation=self.designation,
            employee_code="SRV006",
            is_active=False,
            employment_status="INACTIVE",
        )

        EmployeeService.activate_employee(
            employee=employee,
        )

        employee.refresh_from_db()

        self.assertTrue(
            employee.is_active
        )
        self.assertEqual(
            employee.employment_status,
            "ACTIVE",
        )

    def test_deactivate_employee(self):
        employee = create_employee(
            organization=self.organization,
            branch=self.branch,
            department=self.department,
            designation=self.designation,
            employee_code="SRV007",
        )

        EmployeeService.deactivate_employee(
            employee=employee,
        )

        employee.refresh_from_db()

        self.assertFalse(
            employee.is_active
        )
        self.assertEqual(
            employee.employment_status,
            "INACTIVE",
        )
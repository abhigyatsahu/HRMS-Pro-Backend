from datetime import date

from django.test import TestCase

from apps.employees.models import Employee
from apps.employees.serializers import (
    EmployeeCreateSerializer,
    EmployeeSerializer,
    EmployeeUpdateSerializer,
)
from apps.employees.tests.factories import (
    create_department,
    create_designation,
    create_employee,
    create_organization,
)


class EmployeeSerializerTestCase(TestCase):

    def setUp(self):
        self.organization = create_organization("SER-ORG")

        self.branch = self.organization.branches.create(
            name="Main Branch",
            code="SER-BR",
        )

        self.department = create_department(
            self.organization,
            name="Engineering",
            code="SER-DEP",
        )

        self.designation = create_designation(
            self.organization,
            name="Software Engineer",
            code="SER-DES",
        )

    def get_create_data(self, **overrides):
        data = {
            "employee_code": "SER001",
            "first_name": "John",
            "middle_name": "",
            "last_name": "Doe",
            "date_of_birth": "1998-01-15",
            "gender": "MALE",
            "blood_group": "O+",
            "personal_email": "john@example.com",
            "work_email": "john@company.com",
            "phone": "9876543210",
            "alternate_phone": "",
            "address": "Test Address",
            "city": "Durg",
            "state": "Chhattisgarh",
            "country": "India",
            "postal_code": "491001",
            "organization": str(self.organization.uuid),
            "branch": str(self.branch.uuid),
            "department": str(self.department.uuid),
            "designation": str(self.designation.uuid),
            "joining_date": "2026-01-01",
            "confirmation_date": None,
            "employment_type": "FULL TIME",
            "employment_status": "ACTIVE",
            "reporting_manager": None,
            "is_active": True,
        }

        data.update(overrides)
        return data

    def test_create_serializer_valid_data(self):
        serializer = EmployeeCreateSerializer(
            data=self.get_create_data()
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        employee = serializer.save()

        self.assertEqual(
            employee.employee_code,
            "SER001",
        )
        self.assertEqual(
            employee.organization,
            self.organization,
        )
        self.assertEqual(
            employee.department,
            self.department,
        )

    def test_create_serializer_rejects_invalid_organization(self):
        import uuid

        serializer = EmployeeCreateSerializer(
            data=self.get_create_data(
                organization=str(uuid.uuid4())
            )
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "organization",
            serializer.errors,
        )

    def test_create_serializer_rejects_invalid_branch(self):
        import uuid

        serializer = EmployeeCreateSerializer(
            data=self.get_create_data(
                branch=str(uuid.uuid4())
            )
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "branch",
            serializer.errors,
        )

    def test_create_serializer_rejects_invalid_department(self):
        import uuid

        serializer = EmployeeCreateSerializer(
            data=self.get_create_data(
                department=str(uuid.uuid4())
            )
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "department",
            serializer.errors,
        )

    def test_create_serializer_rejects_invalid_designation(self):
        import uuid

        serializer = EmployeeCreateSerializer(
            data=self.get_create_data(
                designation=str(uuid.uuid4())
            )
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "designation",
            serializer.errors,
        )

    def test_create_serializer_rejects_cross_organization_branch(self):
        other_org = create_organization("OTHER-ORG")

        other_branch = other_org.branches.create(
            name="Other Branch",
            code="OTHER-BR",
        )

        serializer = EmployeeCreateSerializer(
            data=self.get_create_data(
                branch=str(other_branch.uuid)
            )
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "branch",
            serializer.errors,
        )

    def test_create_serializer_rejects_cross_organization_department(self):
        other_org = create_organization("OTHER-DEP-ORG")

        other_department = create_department(
            other_org,
            name="Other Department",
            code="OTHER-DEP",
        )

        serializer = EmployeeCreateSerializer(
            data=self.get_create_data(
                department=str(other_department.uuid)
            )
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "department",
            serializer.errors,
        )

    def test_create_serializer_rejects_cross_organization_designation(self):
        other_org = create_organization("OTHER-DES-ORG")

        other_designation = create_designation(
            other_org,
            name="Other Designation",
            code="OTHER-DES",
        )

        serializer = EmployeeCreateSerializer(
            data=self.get_create_data(
                designation=str(other_designation.uuid)
            )
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "designation",
            serializer.errors,
        )

    def test_reporting_manager_must_belong_to_same_organization(self):
        other_org = create_organization("MANAGER-ORG")

        other_branch = other_org.branches.create(
            name="Manager Branch",
            code="MAN-BR",
        )

        other_department = create_department(
            other_org,
            name="Manager Department",
            code="MAN-DEP",
        )

        other_designation = create_designation(
            other_org,
            name="Manager Designation",
            code="MAN-DES",
        )

        manager = create_employee(
            organization=other_org,
            branch=other_branch,
            department=other_department,
            designation=other_designation,
            employee_code="MAN001",
        )

        serializer = EmployeeCreateSerializer(
            data=self.get_create_data(
                reporting_manager=str(manager.uuid)
            )
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "reporting_manager",
            serializer.errors,
        )

    def test_create_serializer_rejects_deleted_organization(self):
        self.organization.delete()

        serializer = EmployeeCreateSerializer(
            data=self.get_create_data()
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "organization",
            serializer.errors,
        )

    def test_create_serializer_rejects_deleted_department(self):
        self.department.delete()

        serializer = EmployeeCreateSerializer(
            data=self.get_create_data()
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "department",
            serializer.errors,
        )

    def test_update_serializer_valid_data(self):
        employee = create_employee(
            organization=self.organization,
            branch=self.branch,
            department=self.department,
            designation=self.designation,
            employee_code="UP001",
        )

        serializer = EmployeeUpdateSerializer(
            employee,
            data={
                "first_name": "Updated",
                "last_name": "Employee",
            },
            partial=True,
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        updated_employee = serializer.save()

        self.assertEqual(
            updated_employee.first_name,
            "Updated",
        )

    def test_employee_cannot_be_own_reporting_manager(self):
        employee = create_employee(
            organization=self.organization,
            branch=self.branch,
            department=self.department,
            designation=self.designation,
            employee_code="SELF001",
        )

        serializer = EmployeeUpdateSerializer(
            employee,
            data={
                "reporting_manager": str(employee.uuid),
            },
            partial=True,
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "reporting_manager",
            serializer.errors,
        )

    def test_read_serializer_contains_nested_relationships(self):
        employee = create_employee(
            organization=self.organization,
            branch=self.branch,
            department=self.department,
            designation=self.designation,
            employee_code="READ001",
        )

        serializer = EmployeeSerializer(employee)

        data = serializer.data

        self.assertEqual(
            data["employee_code"],
            "READ001",
        )
        self.assertEqual(
            data["full_name"],
            employee.full_name,
        )
        self.assertEqual(
            data["organization"]["uuid"],
            str(self.organization.uuid),
        )
        self.assertEqual(
            data["branch"]["uuid"],
            str(self.branch.uuid),
        )
        self.assertEqual(
            data["department"]["uuid"],
            str(self.department.uuid),
        )
        self.assertEqual(
            data["designation"]["uuid"],
            str(self.designation.uuid),
        )

    def test_read_serializer_exposes_soft_delete_fields(self):
        employee = create_employee(
            organization=self.organization,
            branch=self.branch,
            department=self.department,
            designation=self.designation,
            employee_code="DELETE001",
        )

        employee.delete()
        employee.refresh_from_db()

        serializer = EmployeeSerializer(employee)

        self.assertTrue(
            serializer.data["is_deleted"]
        )
        self.assertIsNotNone(
            serializer.data["deleted_at"]
        )
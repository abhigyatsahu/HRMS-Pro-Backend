from datetime import date

from django.test import TestCase

from apps.departments.models import Department
from apps.designations.models import Designation
from apps.employees.models import Employee
from apps.organization.models import Branch, Organization


class EmployeeModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.organization = Organization.objects.create(
            name="Test Technologies",
            code="TEST",
            email="hr@test.com",
            country="India",
        )

        cls.branch = Branch.objects.create(
            organization=cls.organization,
            name="Bhilai Branch",
            code="BHL",
            city="Bhilai",
            state="Chhattisgarh",
            country="India",
        )

        cls.department = Department.objects.create(
            organization=cls.organization,
            name="Engineering",
            code="ENG",
            description="Engineering Department",
            is_active=True,
        )

        cls.designation = Designation.objects.create(
            organization=cls.organization,
            name="Software Engineer",
            code="SE",
            description="Software Engineer",
            level=1,
            is_active=True,
        )

        cls.employee = Employee.objects.create(
            organization=cls.organization,
            branch=cls.branch,
            department=cls.department,
            designation=cls.designation,
            employee_code="EMP0001",
            first_name="Abhigyat",
            middle_name="Kumar",
            last_name="Sahu",
            date_of_birth=date(1999, 1, 15),
            gender="MALE",
            blood_group="O+",
            personal_email="personal@test.com",
            work_email="abhigyat@test.com",
            phone="9876543210",
            alternate_phone="9123456780",
            address="Test Address",
            city="Bhilai",
            state="Chhattisgarh",
            country="India",
            postal_code="490001",
            joining_date=date(2026, 6, 15),
            confirmation_date=date(2027, 6, 15),
            employment_type="FULL TIME",
            employment_status="ACTIVE",
            is_active=True,
        )

    def test_employee_creation(self):
        self.assertIsNotNone(self.employee.uuid)
        self.assertEqual(self.employee.employee_code, "EMP0001")
        self.assertEqual(self.employee.first_name, "Abhigyat")
        self.assertEqual(self.employee.work_email, "abhigyat@test.com")

    def test_employee_full_name(self):
        self.assertEqual(
            self.employee.full_name,
            "Abhigyat Kumar Sahu",
        )

    def test_employee_str(self):
        self.assertEqual(
            str(self.employee),
            "EMP0001 - Abhigyat Kumar Sahu",
        )

    def test_employee_organization_relationship(self):
        self.assertEqual(
            self.employee.organization,
            self.organization,
        )

    def test_employee_branch_relationship(self):
        self.assertEqual(
            self.employee.branch,
            self.branch,
        )

    def test_employee_department_relationship(self):
        self.assertEqual(
            self.employee.department,
            self.department,
        )

    def test_employee_designation_relationship(self):
        self.assertEqual(
            self.employee.designation,
            self.designation,
        )

    def test_employee_is_active_by_default(self):
        self.assertTrue(self.employee.is_active)

    def test_employee_employment_status(self):
        self.assertEqual(
            self.employee.employment_status,
            "ACTIVE",
        )

    def test_employee_soft_delete_default(self):
        self.assertFalse(self.employee.is_deleted)

    def test_employee_soft_delete(self):
        self.employee.delete()

        self.employee.refresh_from_db()

        self.assertTrue(self.employee.is_deleted)

    def test_employee_restore(self):
        self.employee.delete()

        self.employee.restore()

        self.employee.refresh_from_db()

        self.assertFalse(self.employee.is_deleted)

    def test_deleted_employee_hidden_from_default_manager(self):
        self.employee.delete()

        self.assertFalse(
            Employee.objects.filter(
                uuid=self.employee.uuid
            ).exists()
        )

    def test_deleted_employee_available_from_all_objects(self):
        self.employee.delete()

        self.assertTrue(
            Employee.all_objects.filter(
                uuid=self.employee.uuid
            ).exists()
        )

    def test_employee_reporting_manager(self):
        manager = Employee.objects.create(
            organization=self.organization,
            branch=self.branch,
            department=self.department,
            designation=self.designation,
            employee_code="EMP0002",
            first_name="Manager",
            last_name="User",
            joining_date=date(2026, 1, 1),
            employment_type="FULL TIME",
            employment_status="ACTIVE",
            is_active=True,
        )

        employee = Employee.objects.create(
            organization=self.organization,
            branch=self.branch,
            department=self.department,
            designation=self.designation,
            employee_code="EMP0003",
            first_name="Team",
            last_name="Member",
            joining_date=date(2026, 2, 1),
            employment_type="FULL TIME",
            employment_status="ACTIVE",
            reporting_manager=manager,
            is_active=True,
        )

        self.assertEqual(
            employee.reporting_manager,
            manager,
        )

        self.assertIn(
            employee,
            manager.subordinates.all(),
        )
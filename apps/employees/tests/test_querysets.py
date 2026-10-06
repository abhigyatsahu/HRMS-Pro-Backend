from datetime import date

from django.test import TestCase

from apps.departments.models import Department
from apps.designations.models import Designation
from apps.employees.models import Employee
from apps.organization.models import Branch, Organization


class EmployeeQuerySetTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.organization = Organization.objects.create(
            name="Test Technologies",
            code="TEST",
        )

        cls.branch = Branch.objects.create(
            organization=cls.organization,
            name="Bhilai Branch",
            code="BHL",
        )

        cls.department = Department.objects.create(
            organization=cls.organization,
            name="Engineering",
            code="ENG",
            is_active=True,
        )

        cls.designation = Designation.objects.create(
            organization=cls.organization,
            name="Software Engineer",
            code="SE",
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
            last_name="Sahu",
            work_email="abhigyat@test.com",
            phone="9876543210",
            joining_date=date(2026, 6, 15),
            employment_type="FULL TIME",
            employment_status="ACTIVE",
            is_active=True,
        )

        cls.inactive_employee = Employee.objects.create(
            organization=cls.organization,
            branch=cls.branch,
            department=cls.department,
            designation=cls.designation,
            employee_code="EMP0002",
            first_name="Inactive",
            last_name="Employee",
            joining_date=date(2026, 1, 1),
            employment_type="CONTRACT",
            employment_status="INACTIVE",
            is_active=False,
        )

    def test_active_queryset(self):
        employees = Employee.objects.active()

        self.assertIn(
            self.employee,
            employees,
        )

        self.assertNotIn(
            self.inactive_employee,
            employees,
        )

    def test_inactive_queryset(self):
        employees = Employee.objects.inactive()

        self.assertIn(
            self.inactive_employee,
            employees,
        )

        self.assertNotIn(
            self.employee,
            employees,
        )

    def test_for_organization(self):
        employees = Employee.objects.for_organization(
            self.organization
        )

        self.assertEqual(
            employees.count(),
            2,
        )

    def test_for_branch(self):
        employees = Employee.objects.for_branch(
            self.branch
        )

        self.assertEqual(
            employees.count(),
            2,
        )

    def test_for_department(self):
        employees = Employee.objects.for_department(
            self.department
        )

        self.assertEqual(
            employees.count(),
            2,
        )

    def test_for_designation(self):
        employees = Employee.objects.for_designation(
            self.designation
        )

        self.assertEqual(
            employees.count(),
            2,
        )

    def test_search_by_employee_code(self):
        employees = Employee.objects.search("EMP0001")

        self.assertEqual(
            employees.count(),
            1,
        )

        self.assertEqual(
            employees.first(),
            self.employee,
        )

    def test_search_by_first_name(self):
        employees = Employee.objects.search("Abhigyat")

        self.assertEqual(
            employees.count(),
            1,
        )

        self.assertEqual(
            employees.first(),
            self.employee,
        )

    def test_search_by_last_name(self):
        employees = Employee.objects.search("Sahu")

        self.assertEqual(
            employees.count(),
            1,
        )

        self.assertEqual(
            employees.first(),
            self.employee,
        )

    def test_search_by_work_email(self):
        employees = Employee.objects.search("abhigyat@test.com")

        self.assertEqual(
            employees.count(),
            1,
        )

        self.assertEqual(
            employees.first(),
            self.employee,
        )

    def test_search_by_phone(self):
        employees = Employee.objects.search("9876543210")

        self.assertEqual(
            employees.count(),
            1,
        )

        self.assertEqual(
            employees.first(),
            self.employee,
        )

    def test_empty_search_returns_all_non_deleted_employees(self):
        employees = Employee.objects.search("")

        self.assertEqual(
            employees.count(),
            2,
        )

    def test_whitespace_search_returns_all_non_deleted_employees(self):
        employees = Employee.objects.search("   ")

        self.assertEqual(
            employees.count(),
            2,
        )

    def test_soft_deleted_employee_not_returned(self):
        self.employee.delete()

        employees = Employee.objects.all()

        self.assertNotIn(
            self.employee,
            employees,
        )

        self.assertIn(
            self.inactive_employee,
            employees,
        )
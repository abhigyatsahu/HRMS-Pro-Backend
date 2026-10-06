from datetime import date
from django.utils import timezone
from django.test import TestCase

from apps.departments.models import Department
from apps.designations.models import Designation
from apps.employees.models import Employee
from apps.organization.models import Branch, Organization


class EmployeeSoftDeleteTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.organization = Organization.objects.create(
            name="Soft Delete Technologies",
            code="SDT",
        )

        cls.branch = Branch.objects.create(
            organization=cls.organization,
            name="Main Branch",
            code="MAIN",
        )

        cls.department = Department.objects.create(
            organization=cls.organization,
            name="Engineering",
            code="ENG",
            is_active=True,
        )

        cls.designation = Designation.objects.create(
            organization=cls.organization,
            name="Developer",
            code="DEV",
            level=1,
            is_active=True,
        )

    def create_employee(self, employee_code):
        return Employee.objects.create(
            organization=self.organization,
            branch=self.branch,
            department=self.department,
            designation=self.designation,
            employee_code=employee_code,
            first_name="Test",
            last_name="Employee",
            joining_date=date(2026, 1, 1),
            employment_type="FULL TIME",
            employment_status="ACTIVE",
            is_active=True,
        )

    def test_soft_delete_defaults_to_false(self):
        employee = self.create_employee("SD001")

        self.assertFalse(employee.is_deleted)

    def test_soft_delete_defaults(self):
        employee = self.create_employee("SD001")

        self.assertFalse(employee.is_deleted)
        self.assertIsNone(employee.deleted_at)

    def test_instance_delete_soft_deletes_employee(self):
        employee = self.create_employee("SD002")

        employee.delete()

        employee.refresh_from_db()

        self.assertTrue(employee.is_deleted)

    def test_deleted_employee_hidden_from_objects(self):
        employee = self.create_employee("SD003")

        employee.delete()

        self.assertFalse(
            Employee.objects.filter(
                uuid=employee.uuid
            ).exists()
        )

    def test_deleted_employee_available_from_all_objects(self):
        employee = self.create_employee("SD004")

        employee.delete()

        self.assertTrue(
            Employee.all_objects.filter(
                uuid=employee.uuid
            ).exists()
        )

    def test_restore_employee(self):
        employee = self.create_employee("SD005")

        employee.delete()

        self.assertTrue(
            Employee.all_objects.filter(
                uuid=employee.uuid,
                is_deleted=True,
            ).exists()
        )

        employee.restore()

        employee.refresh_from_db()

        self.assertFalse(employee.is_deleted)

        self.assertTrue(
            Employee.objects.filter(
                uuid=employee.uuid
            ).exists()
        )

    def test_queryset_bulk_delete(self):
        employee_1 = self.create_employee("SD006")
        employee_2 = self.create_employee("SD007")

        deleted_count, _ = Employee.objects.filter(
            uuid__in=[
                employee_1.uuid,
                employee_2.uuid,
            ]
        ).delete()

        self.assertEqual(
            deleted_count,
            2,
        )

        self.assertFalse(
            Employee.objects.filter(
                uuid=employee_1.uuid
            ).exists()
        )

        self.assertFalse(
            Employee.objects.filter(
                uuid=employee_2.uuid
            ).exists()
        )

        self.assertTrue(
            Employee.all_objects.filter(
                uuid=employee_1.uuid,
                is_deleted=True,
            ).exists()
        )

        self.assertTrue(
            Employee.all_objects.filter(
                uuid=employee_2.uuid,
                is_deleted=True,
            ).exists()
        )

    def test_queryset_restore(self):
        employee = self.create_employee("SD008")

        employee.delete()

        restored_count, _ = Employee.all_objects.filter(
            uuid=employee.uuid
        ).restore()

        self.assertEqual(
            restored_count,
            1,
        )

        self.assertTrue(
            Employee.objects.filter(
                uuid=employee.uuid
            ).exists()
        )

        employee.refresh_from_db()

        self.assertFalse(employee.is_deleted)

    def test_deleted_employee_does_not_appear_in_search(self):
        employee = self.create_employee("SD009")

        employee.delete()

        results = Employee.objects.search("SD009")

        self.assertEqual(
            results.count(),
            0,
        )

        results = Employee.all_objects.search("SD009")

        self.assertEqual(
            results.count(),
            1,
        )



    def test_instance_delete_sets_deleted_at(self):
        employee = self.create_employee("SD002")

        before_delete = timezone.now()

        employee.delete()

        after_delete = timezone.now()

        employee.refresh_from_db()

        self.assertTrue(employee.is_deleted)
        self.assertIsNotNone(employee.deleted_at)

        self.assertGreaterEqual(
            employee.deleted_at,
            before_delete,
        )

        self.assertLessEqual(
            employee.deleted_at,
            after_delete,
        )

    def test_restore_clears_deleted_at(self):
        employee = self.create_employee("SD003")

        employee.delete()

        employee.refresh_from_db()

        self.assertTrue(employee.is_deleted)
        self.assertIsNotNone(employee.deleted_at)

        employee.restore()

        employee.refresh_from_db()

        self.assertFalse(employee.is_deleted)
        self.assertIsNone(employee.deleted_at)

    def test_queryset_bulk_delete_sets_deleted_at(self):
        employee_1 = self.create_employee("SD004")
        employee_2 = self.create_employee("SD005")

        Employee.objects.filter(
            uuid__in=[
                employee_1.uuid,
                employee_2.uuid,
            ]
        ).delete()

        employee_1.refresh_from_db()
        employee_2.refresh_from_db()

        self.assertTrue(employee_1.is_deleted)
        self.assertTrue(employee_2.is_deleted)

        self.assertIsNotNone(employee_1.deleted_at)
        self.assertIsNotNone(employee_2.deleted_at)

    def test_queryset_restore_clears_deleted_at(self):
        employee = self.create_employee("SD006")

        employee.delete()

        Employee.all_objects.filter(
            uuid=employee.uuid
        ).restore()

        employee.refresh_from_db()

        self.assertFalse(employee.is_deleted)
        self.assertIsNone(employee.deleted_at)
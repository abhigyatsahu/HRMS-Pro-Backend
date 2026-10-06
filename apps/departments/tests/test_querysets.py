from django.test import TestCase
from apps.departments.models import Department
from apps.departments.tests.factories import (
    create_department,
    create_organization,
)


class DepartmentQuerySetTests(TestCase):

    def setUp(self):
        self.organization = create_organization(
            name="ABC Technologies",
            code="ABC",
        )

        self.other_organization = create_organization(
            name="XYZ Technologies",
            code="XYZ",
        )

        self.active_department = create_department(
            organization=self.organization,
            name="Human Resources",
            code="HR",
            description="Human resources department.",
            is_active=True,
        )

        self.inactive_department = create_department(
            organization=self.organization,
            name="Finance",
            code="FIN",
            description="Finance department.",
            is_active=False,
        )

        self.other_department = create_department(
            organization=self.other_organization,
            name="Engineering",
            code="ENG",
            description="Engineering department.",
            is_active=True,
        )
    def test_active(self):
        departments = (
            self.organization.departments
            .active()
        )

        self.assertEqual(
            departments.count(),
            1,
        )

        self.assertIn(
            self.active_department,
            departments,
        )

        self.assertNotIn(
            self.inactive_department,
            departments,
        )
    def test_inactive(self):
        departments = (
            self.organization.departments
            .inactive()
        )

        self.assertEqual(
            departments.count(),
            1,
        )

        self.assertIn(
            self.inactive_department,
            departments,
        )

        self.assertNotIn(
            self.active_department,
            departments,
        )

    def test_for_organization(self):
        departments = (
            Department.objects
            .for_organization(
                self.organization
            )
        )

        self.assertEqual(
            departments.count(),
            2,
        )

        self.assertIn(
            self.active_department,
            departments,
        )

        self.assertIn(
            self.inactive_department,
            departments,
        )

        self.assertNotIn(
            self.other_department,
            departments,
        )

    def test_search_by_name(self):
        departments = (
            Department.objects
            .search("Human")
        )

        self.assertEqual(
            departments.count(),
            1,
        )

        self.assertEqual(
            departments.first(),
            self.active_department,
        )

    def test_search_by_code(self):
        departments = (
            Department.objects
            .search("FIN")
        )

        self.assertEqual(
            departments.count(),
            1,
        )

        self.assertEqual(
            departments.first(),
            self.inactive_department,
        )

    def test_search_by_description(self):
        departments = (
            Department.objects
            .search("Engineering")
        )

        self.assertEqual(
            departments.count(),
            1,
        )

        self.assertEqual(
            departments.first(),
            self.other_department,
        )

    def test_empty_search_returns_all(self):
        departments = (
            Department.objects
            .search("")
        )

        self.assertEqual(
            departments.count(),
            3,
        )

    def test_whitespace_search_returns_all(self):
        departments = (
            Department.objects
            .search("   ")
        )

        self.assertEqual(
            departments.count(),
            3,
        )
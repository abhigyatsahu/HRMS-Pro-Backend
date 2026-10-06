from django.test import TestCase

from apps.designations.models import Designation
from apps.organization.models import Organization


class DesignationQuerySetTests(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            name="ABC Technologies",
            code="ABC",
            email="hr@abc.com",
            is_active=True,
        )

        self.other_organization = Organization.objects.create(
            name="XYZ Technologies",
            code="XYZ",
            email="hr@xyz.com",
            is_active=True,
        )

        self.active_designation = Designation.objects.create(
            organization=self.organization,
            name="Software Engineer",
            code="SE",
            description="Software engineering role.",
            level=2,
            is_active=True,
        )

        self.inactive_designation = Designation.objects.create(
            organization=self.organization,
            name="Old Engineer",
            code="OE",
            description="Old engineering role.",
            level=3,
            is_active=False,
        )

        self.other_designation = Designation.objects.create(
            organization=self.other_organization,
            name="Software Architect",
            code="SA",
            description="Architecture role.",
            level=4,
            is_active=True,
        )

    def test_active(self):
        results = Designation.objects.active()

        self.assertIn(
            self.active_designation,
            results,
        )

        self.assertNotIn(
            self.inactive_designation,
            results,
        )

    def test_inactive(self):
        results = Designation.objects.inactive()

        self.assertIn(
            self.inactive_designation,
            results,
        )

        self.assertNotIn(
            self.active_designation,
            results,
        )

    def test_for_organization(self):
        results = Designation.objects.for_organization(
            self.organization
        )

        self.assertIn(
            self.active_designation,
            results,
        )

        self.assertIn(
            self.inactive_designation,
            results,
        )

        self.assertNotIn(
            self.other_designation,
            results,
        )

    def test_search_by_name(self):
        results = Designation.objects.search(
            "Software"
        )

        self.assertIn(
            self.active_designation,
            results,
        )

        self.assertIn(
            self.other_designation,
            results,
        )

    def test_search_by_code(self):
        results = Designation.objects.search(
            "OE"
        )

        self.assertIn(
            self.inactive_designation,
            results,
        )

    def test_search_by_description(self):
        results = Designation.objects.search(
            "Architecture"
        )

        self.assertIn(
            self.other_designation,
            results,
        )

    def test_search_empty_value(self):
        results = Designation.objects.search("")

        self.assertEqual(
            results.count(),
            3,
        )

    def test_search_whitespace(self):
        results = Designation.objects.search(
            "   "
        )

        self.assertEqual(
            results.count(),
            3,
        )

    def test_deleted_records_are_excluded(self):
        self.active_designation.delete()

        results = Designation.objects.all()

        self.assertNotIn(
            self.active_designation,
            results,
        )
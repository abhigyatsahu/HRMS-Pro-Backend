from django.test import TestCase

from apps.organization.models import Organization

from .factories import create_organization


class OrganizationQuerySetTests(TestCase):

    def setUp(self):
        self.active_org = create_organization(
            name="ABC Technologies",
            code="ABC",
            email="abc@example.com",
            is_active=True,
        )

        self.inactive_org = create_organization(
            name="XYZ Technologies",
            code="XYZ",
            email="xyz@example.com",
            is_active=False,
        )

    def test_active(self):
        queryset = Organization.objects.active()

        self.assertIn(
            self.active_org,
            queryset,
        )

        self.assertNotIn(
            self.inactive_org,
            queryset,
        )

    def test_inactive(self):
        queryset = Organization.objects.inactive()

        self.assertIn(
            self.inactive_org,
            queryset,
        )

        self.assertNotIn(
            self.active_org,
            queryset,
        )

    def test_search_by_name(self):
        queryset = Organization.objects.search(
            "ABC"
        )

        self.assertIn(
            self.active_org,
            queryset,
        )

    def test_search_by_code(self):
        queryset = Organization.objects.search(
            "ABC"
        )

        self.assertIn(
            self.active_org,
            queryset,
        )

    def test_search_by_email(self):
        queryset = Organization.objects.search(
            "abc@example.com"
        )

        self.assertIn(
            self.active_org,
            queryset,
        )
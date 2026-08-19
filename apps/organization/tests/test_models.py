from django.test import TestCase

from apps.organization.models import Organization

from .factories import create_organization


class OrganizationModelTests(TestCase):

    def test_organization_is_created(self):
        organization = create_organization()

        self.assertIsNotNone(
            organization.uuid
        )

        self.assertEqual(
            organization.name,
            "ABC Technologies",
        )

        self.assertEqual(
            organization.code,
            "ABC",
        )

    def test_organization_is_active_by_default(self):
        organization = Organization.objects.create(
            name="XYZ Technologies",
            code="XYZ",
        )

        self.assertTrue(
            organization.is_active
        )

    def test_organization_string_representation(self):
        organization = create_organization()

        self.assertEqual(
            str(organization),
            "ABC Technologies",
        )

    def test_organization_code_is_unique(self):
        create_organization()

        with self.assertRaises(Exception):
            Organization.objects.create(
                name="Another Company",
                code="ABC",
            )
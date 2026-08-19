from django.test import TestCase

from apps.organization.models import Organization
from apps.organization.services import (
    OrganizationService,
)

from .factories import create_organization


class OrganizationServiceTests(TestCase):

    def test_create_organization(self):
        organization = (
            OrganizationService.create(
                {
                    "name": "New Company",
                    "code": "NEW",
                    "email": "admin@new.com",
                }
            )
        )

        self.assertIsNotNone(
            organization.pk
        )

        self.assertEqual(
            organization.code,
            "NEW",
        )

    def test_duplicate_code_is_rejected(self):
        create_organization(
            code="ABC"
        )

        with self.assertRaises(Exception):
            OrganizationService.create(
                {
                    "name": "Another Company",
                    "code": "ABC",
                }
            )

    def test_update_organization(self):
        organization = create_organization()

        updated = (
            OrganizationService.update(
                organization,
                {
                    "name": "Updated Company",
                },
            )
        )

        self.assertEqual(
            updated.name,
            "Updated Company",
        )

    def test_deactivate_organization(self):
        organization = create_organization()

        OrganizationService.deactivate(
            organization
        )

        organization.refresh_from_db()

        self.assertFalse(
            organization.is_active
        )

    def test_activate_organization(self):
        organization = create_organization(
            is_active=False
        )

        OrganizationService.activate(
            organization
        )

        organization.refresh_from_db()

        self.assertTrue(
            organization.is_active
        )
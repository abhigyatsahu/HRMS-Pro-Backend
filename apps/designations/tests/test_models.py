from django.db import IntegrityError
from django.test import TestCase

from apps.designations.models import Designation
from apps.organization.models import Organization


class DesignationModelTests(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            name="ABC Technologies",
            code="ABC",
            email="hr@abc.com",
            is_active=True,
        )

    def create_designation(
        self,
        name="Software Engineer",
        code="SE",
        level=1,
        is_active=True,
    ):
        return Designation.objects.create(
            organization=self.organization,
            name=name,
            code=code,
            description="Software engineering role.",
            level=level,
            is_active=is_active,
        )

    def test_designation_is_created(self):
        designation = self.create_designation()

        self.assertIsNotNone(
            designation.uuid
        )
        self.assertEqual(
            designation.name,
            "Software Engineer",
        )
        self.assertEqual(
            designation.code,
            "SE",
        )
        self.assertEqual(
            designation.level,
            1,
        )
        self.assertTrue(
            designation.is_active
        )
        self.assertFalse(
            designation.is_deleted
        )

    def test_string_representation(self):
        designation = self.create_designation()

        self.assertEqual(
            str(designation),
            "Software Engineer (SE)",
        )

    def test_designation_code_is_unique_per_organization(self):
        self.create_designation()

        with self.assertRaises(
            IntegrityError
        ):
            self.create_designation(
                name="Senior Engineer",
                code="SE",
            )

    def test_same_code_allowed_for_different_organizations(self):
        self.create_designation()

        another_organization = Organization.objects.create(
            name="XYZ Technologies",
            code="XYZ",
            email="hr@xyz.com",
            is_active=True,
        )

        designation = Designation.objects.create(
            organization=another_organization,
            name="Software Engineer",
            code="SE",
            level=1,
        )

        self.assertIsNotNone(
            designation.pk
        )

    def test_active_and_inactive_designations(self):
        active = self.create_designation(
            name="Active Role",
            code="ACTIVE",
            is_active=True,
        )

        inactive = self.create_designation(
            name="Inactive Role",
            code="INACTIVE",
            is_active=False,
        )

        self.assertTrue(
            active.is_active
        )
        self.assertFalse(
            inactive.is_active
        )
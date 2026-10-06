from django.test import TestCase

from apps.designations.models import Designation
from apps.organization.models import Organization


class DesignationManagerTests(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            name="ABC Technologies",
            code="ABC",
            email="hr@abc.com",
            is_active=True,
        )

        self.designation = Designation.objects.create(
            organization=self.organization,
            name="Software Engineer",
            code="SE",
            level=1,
        )

    def test_default_manager_excludes_deleted_records(self):
        self.designation.delete()

        self.assertFalse(
            Designation.objects.filter(
                uuid=self.designation.uuid
            ).exists()
        )

    def test_all_objects_manager_includes_deleted_records(self):
        self.designation.delete()

        self.assertTrue(
            Designation.all_objects.filter(
                uuid=self.designation.uuid
            ).exists()
        )

    def test_default_manager_returns_non_deleted_records(self):
        self.assertTrue(
            Designation.objects.filter(
                uuid=self.designation.uuid
            ).exists()
        )

    def test_all_objects_returns_non_deleted_records(self):
        self.assertTrue(
            Designation.all_objects.filter(
                uuid=self.designation.uuid
            ).exists()
        )
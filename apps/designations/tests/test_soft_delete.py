from django.test import TestCase

from apps.designations.models import Designation
from apps.organization.models import Organization


class DesignationSoftDeleteTests(TestCase):
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

    def test_soft_delete_default(self):
        self.assertFalse(
            self.designation.is_deleted
        )

    def test_delete_does_not_remove_database_row(self):
        uuid = self.designation.uuid

        self.designation.delete()

        self.assertTrue(
            self.designation.is_deleted
        )

        self.assertTrue(
            Designation.all_objects.filter(
                uuid=uuid
            ).exists()
        )

    def test_deleted_designation_not_returned_by_default_manager(self):
        uuid = self.designation.uuid

        self.designation.delete()

        self.assertFalse(
            Designation.objects.filter(
                uuid=uuid
            ).exists()
        )

    def test_deleted_designation_returned_by_all_objects(self):
        uuid = self.designation.uuid

        self.designation.delete()

        self.assertTrue(
            Designation.all_objects.filter(
                uuid=uuid
            ).exists()
        )

    def test_restore_designation(self):
        self.designation.delete()

        self.assertTrue(
            self.designation.is_deleted
        )

        self.designation.restore()

        self.assertFalse(
            self.designation.is_deleted
        )

        self.assertTrue(
            Designation.objects.filter(
                uuid=self.designation.uuid
            ).exists()
        )

    def test_deleted_queryset(self):
        self.designation.delete()

        self.assertTrue(
            Designation.all_objects.deleted().filter(
                uuid=self.designation.uuid
            ).exists()
        )

    def test_not_deleted_queryset(self):
        self.assertTrue(
            Designation.objects.not_deleted().filter(
                uuid=self.designation.uuid
            ).exists()
        )
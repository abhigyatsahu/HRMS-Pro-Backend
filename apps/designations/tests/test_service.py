from django.test import TestCase
from rest_framework.exceptions import NotFound

from apps.common.exceptions import (
    BusinessRuleException,
    DuplicateResourceException,
)
from apps.designations.models import Designation
from apps.designations.services import DesignationService
from apps.organization.models import Organization


class DesignationServiceTests(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            name="ABC Technologies",
            code="ABC",
            email="hr@abc.com",
            is_active=True,
        )

        self.inactive_organization = (
            Organization.objects.create(
                name="Inactive Technologies",
                code="INA",
                email="hr@inactive.com",
                is_active=False,
            )
        )

        self.designation = Designation.objects.create(
            organization=self.organization,
            name="Software Engineer",
            code="SE",
            description="Software engineering role.",
            level=2,
        )

    def test_create_designation(self):
        designation = DesignationService.create(
            {
                "organization_uuid": (
                    self.organization.uuid
                ),
                "name": "Project Manager",
                "code": "PM",
                "description": "Project management role.",
                "level": 3,
            }
        )

        self.assertIsNotNone(
            designation.pk
        )

        self.assertEqual(
            designation.organization,
            self.organization,
        )

        self.assertEqual(
            designation.code,
            "PM",
        )

        self.assertFalse(
            designation.is_deleted
        )

    def test_create_duplicate_code_raises_conflict(self):
        with self.assertRaises(
            DuplicateResourceException
        ) as context:
            DesignationService.create(
                {
                    "organization_uuid": (
                        self.organization.uuid
                    ),
                    "name": "Senior Engineer",
                    "code": "SE",
                    "level": 3,
                }
            )

        self.assertEqual(
            context.exception.code,
            "duplicate_resource",
        )

        self.assertEqual(
            context.exception.status_code,
            409,
        )

    def test_create_under_inactive_organization_fails(self):
        with self.assertRaises(
            BusinessRuleException
        ):
            DesignationService.create(
                {
                    "organization_uuid": (
                        self.inactive_organization.uuid
                    ),
                    "name": "Project Manager",
                    "code": "PM",
                    "level": 3,
                }
            )

    def test_create_with_invalid_organization_fails(self):
        with self.assertRaises(
            NotFound
        ):
            DesignationService.create(
                {
                    "organization_uuid": (
                        "00000000-0000-0000-0000-000000000000"
                    ),
                    "name": "Project Manager",
                    "code": "PM",
                    "level": 3,
                }
            )

    def test_update_designation(self):
        updated = DesignationService.update(
            self.designation,
            {
                "name": "Senior Software Engineer",
                "code": "SSE",
                "description": "Senior engineering role.",
                "level": 3,
            },
        )

        self.assertEqual(
            updated.name,
            "Senior Software Engineer",
        )

        self.assertEqual(
            updated.code,
            "SSE",
        )

        self.assertEqual(
            updated.level,
            3,
        )

    def test_update_duplicate_code_raises_conflict(self):
        other = Designation.objects.create(
            organization=self.organization,
            name="Project Manager",
            code="PM",
            level=3,
        )

        with self.assertRaises(
            DuplicateResourceException
        ):
            DesignationService.update(
                self.designation,
                {
                    "code": other.code,
                },
            )

    def test_update_same_code_is_allowed(self):
        updated = DesignationService.update(
            self.designation,
            {
                "code": self.designation.code,
            },
        )

        self.assertEqual(
            updated.code,
            "SE",
        )

    def test_activate_designation(self):
        self.designation.is_active = False
        self.designation.save(
            update_fields=["is_active"]
        )

        result = DesignationService.activate(
            self.designation
        )

        self.assertTrue(
            result.is_active
        )

    def test_activate_already_active_designation(self):
        result = DesignationService.activate(
            self.designation
        )

        self.assertTrue(
            result.is_active
        )

    def test_activate_under_inactive_organization_fails(self):
        self.designation.organization = (
            self.inactive_organization
        )
        self.designation.is_active = False
        self.designation.save(
            update_fields=[
                "organization",
                "is_active",
            ]
        )

        with self.assertRaises(
            BusinessRuleException
        ):
            DesignationService.activate(
                self.designation
            )

    def test_deactivate_designation(self):
        result = DesignationService.deactivate(
            self.designation
        )

        self.assertFalse(
            result.is_active
        )

    def test_deactivate_already_inactive_designation(self):
        self.designation.is_active = False
        self.designation.save(
            update_fields=["is_active"]
        )

        result = DesignationService.deactivate(
            self.designation
        )

        self.assertFalse(
            result.is_active
        )

    def test_delete_soft_deletes_designation(self):
        result = DesignationService.delete(
            self.designation
        )

        self.assertTrue(
            result.is_deleted
        )

        self.assertTrue(
            Designation.all_objects.filter(
                pk=self.designation.pk
            ).exists()
        )

        self.assertFalse(
            Designation.objects.filter(
                pk=self.designation.pk
            ).exists()
        )

    def test_delete_already_deleted_designation(self):
        self.designation.delete()

        result = DesignationService.delete(
            self.designation
        )

        self.assertTrue(
            result.is_deleted
        )

    def test_restore_designation(self):
        self.designation.delete()

        result = DesignationService.restore(
            self.designation
        )

        self.assertFalse(
            result.is_deleted
        )

        self.assertTrue(
            Designation.objects.filter(
                pk=self.designation.pk
            ).exists()
        )

    def test_restore_already_active_designation(self):
        result = DesignationService.restore(
            self.designation
        )

        self.assertFalse(
            result.is_deleted
        )

    def test_restore_conflicting_code_raises_conflict(self):
        self.designation.delete()

        Designation.objects.create(
            organization=self.organization,
            name="New Software Engineer",
            code="SE",
            level=2,
        )

        with self.assertRaises(
            DuplicateResourceException
        ):
            DesignationService.restore(
                self.designation
            )

    def test_restore_under_inactive_organization_fails(self):
        self.designation.delete()

        self.organization.is_active = False
        self.organization.save(
            update_fields=["is_active"]
        )

        with self.assertRaises(
            BusinessRuleException
        ):
            DesignationService.restore(
                self.designation
            )

    def test_deleted_code_can_be_reused(self):
        self.designation.delete()

        new_designation = (
            DesignationService.create(
                {
                    "organization_uuid": (
                        self.organization.uuid
                    ),
                    "name": "New Software Engineer",
                    "code": "SE",
                    "level": 2,
                }
            )
        )

        self.assertIsNotNone(
            new_designation.pk
        )

        self.assertEqual(
            new_designation.code,
            "SE",
        )
from django.test import TestCase
from rest_framework.exceptions import NotFound

from apps.common.exceptions import (
    BusinessRuleException,
    DuplicateResourceException,
)
from apps.departments.models import Department
from apps.departments.services import (
    DepartmentService,
)
from apps.departments.tests.factories import (
    create_department,
    create_organization,
)


class DepartmentCreateServiceTests(TestCase):

    def setUp(self):
        self.organization = create_organization(
            name="ABC Technologies",
            code="ABC",
        )

    def test_create_department(self):
        department = DepartmentService.create(
            {
                "organization_uuid": (
                    self.organization.uuid
                ),
                "name": "Human Resources",
                "code": "HR",
                "description": (
                    "Human resources department."
                ),
            }
        )

        self.assertIsInstance(
            department,
            Department,
        )

        self.assertEqual(
            department.name,
            "Human Resources",
        )

        self.assertEqual(
            department.code,
            "HR",
        )

        self.assertEqual(
            department.organization,
            self.organization,
        )

    def test_duplicate_department_code_raises_conflict(
        self,
    ):
        create_department(
            organization=self.organization,
            name="Human Resources",
            code="HR",
        )

        with self.assertRaises(
            DuplicateResourceException
        ) as context:

            DepartmentService.create(
                {
                    "organization_uuid": (
                        self.organization.uuid
                    ),
                    "name": "Human Resources 2",
                    "code": "HR",
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

    def test_same_code_allowed_for_different_organization(
        self,
    ):
        other_organization = create_organization(
            name="XYZ Technologies",
            code="XYZ",
        )

        create_department(
            organization=self.organization,
            code="HR",
        )

        department = DepartmentService.create(
            {
                "organization_uuid": (
                    other_organization.uuid
                ),
                "name": "Human Resources",
                "code": "HR",
            }
        )

        self.assertEqual(
            department.code,
            "HR",
        )

        self.assertEqual(
            department.organization,
            other_organization,
        )

    def test_inactive_organization_cannot_create_department(
        self,
    ):
        self.organization.is_active = False

        self.organization.save(
            update_fields=["is_active"]
        )

        with self.assertRaises(
            BusinessRuleException
        ):
            DepartmentService.create(
                {
                    "organization_uuid": (
                        self.organization.uuid
                    ),
                    "name": "Human Resources",
                    "code": "HR",
                }
            )

    def test_missing_organization_raises_not_found(
        self,
    ):
        import uuid

        with self.assertRaises(
            NotFound
        ):
            DepartmentService.create(
                {
                    "organization_uuid": uuid.uuid4(),
                    "name": "Human Resources",
                    "code": "HR",
                }
            )


class DepartmentUpdateServiceTests(TestCase):

    def setUp(self):
        self.organization = create_organization(
            name="ABC Technologies",
            code="ABC",
        )

        self.department = create_department(
            organization=self.organization,
            name="Human Resources",
            code="HR",
        )

    def test_update_department(self):
        department = DepartmentService.update(
            self.department,
            {
                "name": "People Operations",
                "description": (
                    "Updated description."
                ),
            },
        )

        department.refresh_from_db()

        self.assertEqual(
            department.name,
            "People Operations",
        )

        self.assertEqual(
            department.description,
            "Updated description.",
        )

    def test_update_department_code(self):
        department = DepartmentService.update(
            self.department,
            {
                "code": "PEOPLE",
            },
        )

        department.refresh_from_db()

        self.assertEqual(
            department.code,
            "PEOPLE",
        )

    def test_update_duplicate_code_raises_conflict(
        self,
    ):
        create_department(
            organization=self.organization,
            name="Finance",
            code="FIN",
        )

        with self.assertRaises(
            DuplicateResourceException
        ) as context:

            DepartmentService.update(
                self.department,
                {
                    "code": "FIN",
                },
            )

        self.assertEqual(
            context.exception.code,
            "duplicate_resource",
        )

    def test_update_same_code_is_allowed(
        self,
    ):
        department = DepartmentService.update(
            self.department,
            {
                "code": "HR",
            },
        )

        self.assertEqual(
            department.code,
            "HR",
        )


class DepartmentStatusServiceTests(TestCase):

    def setUp(self):
        self.organization = create_organization(
            name="ABC Technologies",
            code="ABC",
        )

        self.department = create_department(
            organization=self.organization,
            code="HR",
            is_active=True,
        )

    def test_deactivate_department(self):
        department = (
            DepartmentService.deactivate(
                self.department
            )
        )

        department.refresh_from_db()

        self.assertFalse(
            department.is_active
        )

    def test_deactivate_already_inactive_department(
        self,
    ):
        self.department.is_active = False

        self.department.save(
            update_fields=["is_active"]
        )

        department = (
            DepartmentService.deactivate(
                self.department
            )
        )

        self.assertFalse(
            department.is_active
        )

    def test_activate_department(self):
        self.department.is_active = False

        self.department.save(
            update_fields=["is_active"]
        )

        department = (
            DepartmentService.activate(
                self.department
            )
        )

        department.refresh_from_db()

        self.assertTrue(
            department.is_active
        )

    def test_activate_already_active_department(
        self,
    ):
        department = (
            DepartmentService.activate(
                self.department
            )
        )

        self.assertTrue(
            department.is_active
        )

    def test_cannot_activate_for_inactive_organization(
        self,
    ):
        self.department.is_active = False
        self.department.save(
            update_fields=["is_active"]
        )

        self.organization.is_active = False
        self.organization.save(
            update_fields=["is_active"]
        )

        with self.assertRaises(
            BusinessRuleException
        ):
            DepartmentService.activate(
                self.department
            )
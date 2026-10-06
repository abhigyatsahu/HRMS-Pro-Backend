from django.test import TestCase
from rest_framework.exceptions import ValidationError

from apps.departments.serializers import (
    DepartmentCreateSerializer,
    DepartmentSerializer,
    DepartmentUpdateSerializer,
)
from apps.departments.tests.factories import (
    create_department,
    create_organization,
)


class DepartmentSerializerTests(TestCase):

    def setUp(self):
        self.organization = create_organization(
            name="ABC Technologies",
            code="ABC",
        )

    def test_create_serializer_valid_data(self):
        serializer = DepartmentCreateSerializer(
            data={
                "organization_uuid": (
                    str(self.organization.uuid)
                ),
                "name": "Human Resources",
                "code": "hr",
                "description": (
                    "Human resources department."
                ),
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        self.assertEqual(
            serializer.validated_data["code"],
            "HR",
        )

        self.assertEqual(
            serializer.validated_data["name"],
            "Human Resources",
        )

    def test_create_serializer_invalid_organization(
        self,
    ):
        import uuid

        serializer = DepartmentCreateSerializer(
            data={
                "organization_uuid": str(
                    uuid.uuid4()
                ),
                "name": "Human Resources",
                "code": "HR",
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "organization_uuid",
            serializer.errors,
        )

    def test_create_serializer_inactive_organization(
        self,
    ):
        self.organization.is_active = False
        self.organization.save(
            update_fields=["is_active"]
        )

        serializer = DepartmentCreateSerializer(
            data={
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "Human Resources",
                "code": "HR",
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "organization_uuid",
            serializer.errors,
        )

    def test_code_is_normalized(self):
        serializer = DepartmentCreateSerializer(
            data={
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "Human Resources",
                "code": " hr ",
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        self.assertEqual(
            serializer.validated_data["code"],
            "HR",
        )

    def test_name_is_trimmed(self):
        serializer = DepartmentCreateSerializer(
            data={
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "  Human Resources  ",
                "code": "HR",
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        self.assertEqual(
            serializer.validated_data["name"],
            "Human Resources",
        )

    def test_update_serializer_does_not_allow_organization(
        self,
    ):
        serializer = DepartmentUpdateSerializer(
            data={
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "Updated Department",
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertNotIn(
            "organization_uuid",
            serializer.validated_data,
        )

    def test_update_serializer_normalizes_code(self):
        department = create_department(
            organization=self.organization,
            code="HR",
        )

        serializer = DepartmentUpdateSerializer(
            department,
            data={
                "code": " finance ",
            },
            partial=True,
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        self.assertEqual(
            serializer.validated_data["code"],
            "FINANCE",
        )

    def test_response_serializer(self):
        department = create_department(
            organization=self.organization,
            name="Human Resources",
            code="HR",
        )

        serializer = DepartmentSerializer(
            department
        )

        self.assertEqual(
            serializer.data["uuid"],
            str(department.uuid),
        )

        self.assertEqual(
            serializer.data["organization_uuid"],
            str(self.organization.uuid),
        )

        self.assertEqual(
            serializer.data["organization_name"],
            "ABC Technologies",
        )

        self.assertEqual(
            serializer.data["code"],
            "HR",
        )
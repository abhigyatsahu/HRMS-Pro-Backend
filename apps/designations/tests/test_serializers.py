from django.test import TestCase

from apps.designations.models import Designation
from apps.designations.serializers import (
    DesignationSerializer,
    DesignationCreateSerializer,
    DesignationUpdateSerializer,
)
from apps.organization.models import Organization


class DesignationSerializerTests(TestCase):
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
            description="Software engineering role.",
            level=2,
        )

    def test_designation_serializer_contains_expected_fields(self):
        serializer = DesignationSerializer(
            self.designation
        )

        data = serializer.data

        self.assertEqual(
            data["uuid"],
            str(self.designation.uuid),
        )

        self.assertEqual(
            data["organization_uuid"],
            str(self.organization.uuid),
        )

        self.assertEqual(
            data["organization_name"],
            self.organization.name,
        )

        self.assertEqual(
            data["name"],
            "Software Engineer",
        )

        self.assertEqual(
            data["code"],
            "SE",
        )

        self.assertEqual(
            data["level"],
            2,
        )

        self.assertFalse(
            "is_deleted" in data
        )

    def test_create_serializer_valid_data(self):
        serializer = DesignationCreateSerializer(
            data={
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "Project Manager",
                "code": "PM",
                "description": "Project management role.",
                "level": 3,
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

    def test_create_serializer_normalizes_name(self):
        serializer = DesignationCreateSerializer(
            data={
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "  Project Manager  ",
                "code": "pm",
                "level": 3,
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        self.assertEqual(
            serializer.validated_data["name"],
            "Project Manager",
        )

        self.assertEqual(
            serializer.validated_data["code"],
            "PM",
        )

    def test_create_serializer_rejects_missing_organization(self):
        serializer = DesignationCreateSerializer(
            data={
                "organization_uuid": (
                    "00000000-0000-0000-0000-000000000000"
                ),
                "name": "Project Manager",
                "code": "PM",
                "level": 3,
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "organization_uuid",
            serializer.errors,
        )

    def test_create_serializer_rejects_inactive_organization(self):
        self.organization.is_active = False
        self.organization.save(
            update_fields=["is_active"]
        )

        serializer = DesignationCreateSerializer(
            data={
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "Project Manager",
                "code": "PM",
                "level": 3,
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "organization_uuid",
            serializer.errors,
        )

    def test_create_serializer_rejects_empty_name(self):
        serializer = DesignationCreateSerializer(
            data={
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "   ",
                "code": "PM",
                "level": 3,
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "name",
            serializer.errors,
        )

    def test_create_serializer_rejects_empty_code(self):
        serializer = DesignationCreateSerializer(
            data={
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "Project Manager",
                "code": "   ",
                "level": 3,
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "code",
            serializer.errors,
        )

    def test_create_serializer_rejects_invalid_level(self):
        serializer = DesignationCreateSerializer(
            data={
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "Project Manager",
                "code": "PM",
                "level": 0,
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "level",
            serializer.errors,
        )

    def test_update_serializer_valid_data(self):
        serializer = DesignationUpdateSerializer(
            self.designation,
            data={
                "name": "Senior Software Engineer",
                "code": "SSE",
                "description": "Senior engineering role.",
                "level": 3,
            },
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

    def test_update_serializer_normalizes_code(self):
        serializer = DesignationUpdateSerializer(
            self.designation,
            data={
                "code": "  sse  ",
            },
            partial=True,
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        self.assertEqual(
            serializer.validated_data["code"],
            "SSE",
        )

    def test_update_serializer_rejects_invalid_level(self):
        serializer = DesignationUpdateSerializer(
            self.designation,
            data={
                "level": 0,
            },
            partial=True,
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "level",
            serializer.errors,
        )
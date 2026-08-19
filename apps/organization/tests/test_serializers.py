from django.test import TestCase

from apps.organization.serializers import (
    OrganizationCreateSerializer,
)


class OrganizationSerializerTests(TestCase):

    def test_valid_data(self):
        serializer = (
            OrganizationCreateSerializer(
                data={
                    "name": "   ABC    Technologies   ",
                    "code": "abc",
                    "email": "admin@abc.com",
                }
            )
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

        self.assertEqual(
            serializer.validated_data["name"],
            "ABC Technologies",
        )

        self.assertEqual(
            serializer.validated_data["code"],
            "ABC",
        )

    def test_invalid_email(self):
        serializer = (
            OrganizationCreateSerializer(
                data={
                    "name": "ABC",
                    "code": "ABC",
                    "email": "invalid",
                }
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "email",
            serializer.errors,
        )

    def test_missing_required_fields(self):
        serializer = (
            OrganizationCreateSerializer(
                data={}
            )
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "name",
            serializer.errors,
        )

        self.assertIn(
            "code",
            serializer.errors,
        )
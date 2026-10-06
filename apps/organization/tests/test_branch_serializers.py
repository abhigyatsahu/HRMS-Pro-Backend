from django.test import TestCase

from apps.organization.serializers import (
    BranchCreateSerializer,
    BranchSerializer,
    BranchUpdateSerializer,
)

from .factories import (
    create_branch,
    create_organization,
)


class BranchCreateSerializerTests(
    TestCase
):

    def setUp(self):
        self.organization = create_organization()

    def test_valid_data(self):
        serializer = BranchCreateSerializer(
            data={
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "  Raipur Branch  ",
                "code": " rai ",
                "city": "Raipur",
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

    def test_name_is_normalized(self):
        serializer = BranchCreateSerializer(
            data={
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "  Raipur Branch  ",
                "code": "RAI",
            }
        )

        self.assertTrue(
            serializer.is_valid()
        )

        self.assertEqual(
            serializer.validated_data["name"],
            "Raipur Branch",
        )

    def test_code_is_uppercase(self):
        serializer = BranchCreateSerializer(
            data={
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "Raipur Branch",
                "code": "rai",
            }
        )

        self.assertTrue(
            serializer.is_valid()
        )

        self.assertEqual(
            serializer.validated_data["code"],
            "RAI",
        )

    def test_invalid_organization(self):
        import uuid

        serializer = BranchCreateSerializer(
            data={
                "organization_uuid": str(
                    uuid.uuid4()
                ),
                "name": "Test Branch",
                "code": "TEST",
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "organization_uuid",
            serializer.errors,
        )

    def test_inactive_organization(self):
        self.organization.is_active = False
        self.organization.save(
            update_fields=["is_active"]
        )

        serializer = BranchCreateSerializer(
            data={
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "Test Branch",
                "code": "TEST",
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "organization_uuid",
            serializer.errors,
        )


class BranchUpdateSerializerTests(
    TestCase
):

    def setUp(self):
        self.organization = create_organization()

        self.branch = create_branch(
            self.organization
        )

    def test_update_name(self):
        serializer = BranchUpdateSerializer(
            self.branch,
            data={
                "name": "Updated Branch",
            },
            partial=True,
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors,
        )

    def test_update_code_normalizes(self):
        serializer = BranchUpdateSerializer(
            self.branch,
            data={
                "code": "new001",
            },
            partial=True,
        )

        self.assertTrue(
            serializer.is_valid()
        )

        self.assertEqual(
            serializer.validated_data["code"],
            "NEW001",
        )


class BranchSerializerTests(TestCase):

    def setUp(self):
        self.organization = create_organization()

        self.branch = create_branch(
            self.organization,
            name="Raipur Branch",
            code="RAI",
        )

    def test_response_serializer(self):
        serializer = BranchSerializer(
            self.branch
        )

        data = serializer.data

        self.assertEqual(
            data["name"],
            "Raipur Branch",
        )

        self.assertEqual(
            data["code"],
            "RAI",
        )

        self.assertEqual(
            data["organization_uuid"],
            str(
                self.organization.uuid
            ),
        )

        self.assertEqual(
            data["organization_name"],
            self.organization.name,
        )
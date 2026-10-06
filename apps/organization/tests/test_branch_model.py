from django.test import TestCase

from apps.organization.models import Branch

from .factories import (
    create_branch,
    create_organization,
)


class BranchModelTests(TestCase):

    def setUp(self):
        self.organization = create_organization()

    def test_branch_can_be_created(self):
        branch = create_branch(
            self.organization
        )

        self.assertIsNotNone(
            branch.uuid
        )

        self.assertEqual(
            branch.name,
            "Test Branch",
        )

        self.assertEqual(
            branch.code,
            "BR001",
        )

        self.assertEqual(
            branch.organization,
            self.organization,
        )

    def test_branch_defaults_to_active(self):
        branch = create_branch(
            self.organization
        )

        self.assertTrue(
            branch.is_active
        )

    def test_branch_string_representation(self):
        branch = create_branch(
            self.organization,
            name="Raipur Branch",
            code="RAI",
        )

        self.assertIn(
            "Raipur Branch",
            str(branch),
        )
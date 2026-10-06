from django.test import TestCase

from apps.common.exceptions import (
    BusinessRuleException,
    DuplicateResourceException,
)
from apps.organization.services import (
    BranchService,
)

from .factories import (
    create_branch,
    create_organization,
)

class BranchCreateServiceTests(
    TestCase
):

    def setUp(self):
        self.organization = create_organization(
            code="ORG001"
        )

    def test_create_branch(self):
        branch = BranchService.create(
            {
                "organization_uuid": (
                    self.organization.uuid
                ),
                "name": "Raipur Branch",
                "code": "RAI",
                "city": "Raipur",
            }
        )

        self.assertIsNotNone(
            branch.pk
        )

        self.assertEqual(
            branch.name,
            "Raipur Branch",
        )

        self.assertEqual(
            branch.code,
            "RAI",
        )

        self.assertEqual(
            branch.organization,
            self.organization,
        )

    def test_duplicate_branch_code_raises_conflict(
        self,
    ):
        create_branch(
            self.organization,
            code="RAI",
        )

        with self.assertRaises(
            DuplicateResourceException
        ) as context:

            BranchService.create(
                {
                    "organization_uuid": (
                        self.organization.uuid
                    ),
                    "name": "Another Branch",
                    "code": "RAI",
                }
            )

        self.assertEqual(
            context.exception.status_code,
            409,
        )

        self.assertEqual(
            context.exception.code,
            "duplicate_resource",
        )

    def test_inactive_organization_cannot_create_branch(
        self,
    ):
        self.organization.is_active = False

        self.organization.save(
            update_fields=["is_active"]
        )

        with self.assertRaises(
            BusinessRuleException
        ):

            BranchService.create(
                {
                    "organization_uuid": (
                        self.organization.uuid
                    ),
                    "name": "Test Branch",
                    "code": "TEST",
                }
            )
class BranchUpdateServiceTests(
    TestCase
):

    def setUp(self):
        self.organization = create_organization(
            code="ORG001"
        )

        self.branch = create_branch(
            self.organization,
            name="Original Branch",
            code="BR001",
        )

    def test_update_branch_name(self):
        branch = BranchService.update(
            self.branch,
            {
                "name": "Updated Branch",
            },
        )

        branch.refresh_from_db()

        self.assertEqual(
            branch.name,
            "Updated Branch",
        )

    def test_duplicate_code_on_update(
        self,
    ):
        create_branch(
            self.organization,
            name="Second Branch",
            code="BR002",
        )

        with self.assertRaises(
            DuplicateResourceException
        ):

            BranchService.update(
                self.branch,
                {
                    "code": "BR002",
                },
            )

class BranchStatusServiceTests(
    TestCase
):

    def setUp(self):
        self.organization = create_organization(
            code="ORG001"
        )

        self.branch = create_branch(
            self.organization,
            is_active=True,
        )

    def test_deactivate_branch(self):
        branch = BranchService.deactivate(
            self.branch
        )

        branch.refresh_from_db()

        self.assertFalse(
            branch.is_active
        )

    def test_activate_branch(self):
        self.branch.is_active = False

        self.branch.save(
            update_fields=[
                "is_active"
            ]
        )

        branch = BranchService.activate(
            self.branch
        )

        branch.refresh_from_db()

        self.assertTrue(
            branch.is_active
        )

    def test_cannot_activate_when_organization_inactive(
        self,
    ):
        self.branch.is_active = False

        self.branch.save(
            update_fields=[
                "is_active"
            ]
        )

        self.organization.is_active = False

        self.organization.save(
            update_fields=[
                "is_active"
            ]
        )

        with self.assertRaises(
            BusinessRuleException
        ):

            BranchService.activate(
                self.branch
            )
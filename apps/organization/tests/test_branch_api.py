from rest_framework import status
from rest_framework.test import (
    APITestCase,
)

from apps.organization.models import Branch

from .factories import (
    create_branch,
    create_organization,
    create_user,
)

class BranchAPITests(APITestCase):

    def setUp(self):
        self.user = create_user()

        self.organization = (
            create_organization(
                code="ORG001"
            )
        )

        self.branch = create_branch(
            self.organization,
            name="Raipur Branch",
            code="RAI",
        )

        self.client.force_authenticate(
            user=self.user
        )

        self.list_url = (
            "/api/v1/organizations/branches/"
        )

    def test_list_branches(self):
        response = self.client.get(
            self.list_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
    def test_create_branch(self):
        response = self.client.post(
            self.list_url,
            {
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "Delhi Branch",
                "code": "DEL",
                "city": "Delhi",
                "state": "Delhi",
                "country": "India",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            response.data["success"]
        )

        self.assertEqual(
            response.data["message"],
            "Branch created successfully.",
        )

        self.assertTrue(
            Branch.objects.filter(
                organization=self.organization,
                code="DEL",
            ).exists()
        )
    def test_duplicate_branch_returns_409(
        self,
    ):
        response = self.client.post(
            self.list_url,
            {
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "Another Raipur Branch",
                "code": "RAI",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_409_CONFLICT,
        )

        self.assertFalse(
            response.data["success"]
        )

        self.assertEqual(
            response.data["errors"]["code"],
            "duplicate_resource",
        )
    def test_retrieve_branch(self):
        url = (
            f"{self.list_url}"
            f"{self.branch.uuid}/"
        )

        response = self.client.get(
            url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"]
        )

        self.assertEqual(
            response.data["data"]["uuid"],
            str(self.branch.uuid),
        )
    def test_update_branch(self):
        url = (
            f"{self.list_url}"
            f"{self.branch.uuid}/"
        )

        response = self.client.patch(
            url,
            {
                "name": "Updated Raipur Branch",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.branch.refresh_from_db()

        self.assertEqual(
            self.branch.name,
            "Updated Raipur Branch",
        )
    def test_deactivate_branch(self):
        url = (
            f"{self.list_url}"
            f"{self.branch.uuid}/deactivate/"
        )

        response = self.client.post(
            url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.branch.refresh_from_db()

        self.assertFalse(
            self.branch.is_active
        )
    def test_activate_branch(self):
        self.branch.is_active = False

        self.branch.save(
            update_fields=[
                "is_active"
            ]
        )

        url = (
            f"{self.list_url}"
            f"{self.branch.uuid}/activate/"
        )

        response = self.client.post(
            url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.branch.refresh_from_db()

        self.assertTrue(
            self.branch.is_active
        )
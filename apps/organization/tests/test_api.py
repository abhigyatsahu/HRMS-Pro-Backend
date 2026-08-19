from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from apps.accounts.models import User

from .factories import create_organization


class OrganizationAPITests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="Admin@123",
            role=User.Role.ADMIN,
        )

        self.employee = User.objects.create_user(
            username="employee",
            email="employee@test.com",
            password="Employee@123",
            role=User.Role.EMPLOYEE,
        )

        self.organization = create_organization()

    def authenticate_admin(self):
        self.client.force_authenticate(
            user=self.admin
        )

    def test_admin_can_list_organizations(self):
        self.authenticate_admin()

        response = self.client.get(
            "/api/v1/organizations/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTrue(
            response.data["success"]
        )

    def test_admin_can_create_organization(self):
        self.authenticate_admin()

        response = self.client.post(
            "/api/v1/organizations/",
            {
                "name": "New Company",
                "code": "NEW",
                "email": "admin@new.com",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        self.assertTrue(
            response.data["success"]
        )

        self.assertEqual(
            response.data["data"]["code"],
            "NEW",
        )

    def test_employee_cannot_create_organization(self):
        self.client.force_authenticate(
            user=self.employee
        )

        response = self.client.post(
            "/api/v1/organizations/",
            {
                "name": "Unauthorized Company",
                "code": "UNAUTH",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_employee_cannot_list_organizations(self):
        self.client.force_authenticate(
            user=self.employee
        )

        response = self.client.get(
            "/api/v1/organizations/"
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_admin_can_retrieve_organization(self):
        self.authenticate_admin()

        response = self.client.get(
            f"/api/v1/organizations/"
            f"{self.organization.uuid}/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertTrue(
            response.data["success"]
        )

        self.assertEqual(
            response.data["data"]["uuid"],
            str(self.organization.uuid),
        )

    def test_admin_can_update_organization(self):
        self.authenticate_admin()

        response = self.client.patch(
            f"/api/v1/organizations/"
            f"{self.organization.uuid}/",
            {
                "name": "Updated Company",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.organization.refresh_from_db()

        self.assertEqual(
            self.organization.name,
            "Updated Company",
        )

    def test_admin_can_deactivate_organization(self):
        self.authenticate_admin()

        response = self.client.post(
            f"/api/v1/organizations/"
            f"{self.organization.uuid}/deactivate/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.organization.refresh_from_db()

        self.assertFalse(
            self.organization.is_active
        )

    def test_admin_can_activate_organization(self):
        self.authenticate_admin()

        self.organization.is_active = False
        self.organization.save()

        response = self.client.post(
            f"/api/v1/organizations/"
            f"{self.organization.uuid}/activate/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.organization.refresh_from_db()

        self.assertTrue(
            self.organization.is_active
        )

    def test_unauthenticated_user_cannot_access_organizations(self):
        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            "/api/v1/organizations/"
        )

        self.assertEqual(
            response.status_code,
            401,
        )
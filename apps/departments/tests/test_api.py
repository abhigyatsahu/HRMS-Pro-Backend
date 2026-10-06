from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.departments.models import Department
from apps.departments.tests.factories import (
    create_department,
    create_organization,
)


class DepartmentAPITests(APITestCase):

    def setUp(self):
        self.organization = create_organization(
            name="ABC Technologies",
            code="ABC",
        )

        self.admin = User.objects.create_user(
            username="admin",
            email="admin@example.com",
            password="Admin@123",
            role=User.Role.ADMIN,
        )

        self.hr_manager = User.objects.create_user(
            username="hrmanager",
            email="hr@example.com",
            password="HR@123",
            role=User.Role.HR_MANAGER,
        )

        self.employee = User.objects.create_user(
            username="employee",
            email="employee@example.com",
            password="Employee@123",
            role=User.Role.EMPLOYEE,
        )

        self.department = create_department(
            organization=self.organization,
            name="Human Resources",
            code="HR",
            description="HR department",
        )

        self.list_url = reverse(
            "department-list-create"
        )

        self.detail_url = reverse(
            "department-detail",
            kwargs={
                "uuid": self.department.uuid,
            },
        )

        self.activate_url = reverse(
            "department-activate",
            kwargs={
                "uuid": self.department.uuid,
            },
        )

        self.deactivate_url = reverse(
            "department-deactivate",
            kwargs={
                "uuid": self.department.uuid,
            },
        )

    def test_list_requires_authentication(self):
        response = self.client.get(
            self.list_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_create_requires_authentication(self):
        response = self.client.post(
            self.list_url,
            {
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "Finance",
                "code": "FIN",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_employee_cannot_list_departments(self):
        self.client.force_authenticate(
            user=self.employee
        )

        response = self.client.get(
            self.list_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_hr_manager_can_list_departments(self):
        self.client.force_authenticate(
            user=self.hr_manager
        )

        response = self.client.get(
            self.list_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"]
        )

    def test_hr_manager_cannot_create_department(self):
        self.client.force_authenticate(
            user=self.hr_manager
        )

        response = self.client.post(
            self.list_url,
            {
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "Finance",
                "code": "FIN",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_list_departments(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.get(
            self.list_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"]
        )

        self.assertEqual(
            response.data["message"],
            "Data fetched successfully.",
        )

        self.assertIn(
            "data",
            response.data,
        )

    def test_search_departments(self):
        create_department(
            organization=self.organization,
            name="Finance",
            code="FIN",
        )

        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.get(
            self.list_url,
            {
                "search": "Finance",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_ordering_departments(self):
        create_department(
            organization=self.organization,
            name="Finance",
            code="FIN",
        )

        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.get(
            self.list_url,
            {
                "ordering": "name",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_create_department(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            self.list_url,
            {
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "Finance",
                "code": "FIN",
                "description": (
                    "Finance department"
                ),
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
            "Department created successfully.",
        )

        self.assertTrue(
            Department.objects.filter(
                organization=self.organization,
                code="FIN",
            ).exists()
        )

    def test_duplicate_department_returns_409(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            self.list_url,
            {
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "Human Resources 2",
                "code": "HR",
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
            response.data["message"],
            "Department code 'HR' already exists "
            "for this organization.",
        )

        self.assertEqual(
            response.data["errors"]["code"],
            "duplicate_resource",
        )

    def test_retrieve_department(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.get(
            self.detail_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"]
        )

        self.assertEqual(
            response.data["data"]["code"],
            "HR",
        )

        self.assertEqual(
            response.data["data"]["organization_name"],
            "ABC Technologies",
        )

    def test_update_department(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.patch(
            self.detail_url,
            {
                "name": "People Operations",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"]
        )

        self.assertEqual(
            response.data["data"]["name"],
            "People Operations",
        )

    def test_update_duplicate_code_returns_409(self):
        create_department(
            organization=self.organization,
            name="Finance",
            code="FIN",
        )

        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.patch(
            self.detail_url,
            {
                "code": "FIN",
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

    def test_activate_department(self):
        self.department.is_active = False

        self.department.save(
            update_fields=["is_active"]
        )

        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            self.activate_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"]
        )

        self.assertEqual(
            response.data["message"],
            "Department activated successfully.",
        )

        self.assertTrue(
            response.data["data"]["is_active"]
        )

    def test_deactivate_department(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.post(
            self.deactivate_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"]
        )

        self.assertEqual(
            response.data["message"],
            "Department deactivated successfully.",
        )

        self.assertFalse(
            response.data["data"]["is_active"]
        )

    def test_hr_manager_cannot_activate_department(
        self,
    ):
        self.department.is_active = False

        self.department.save(
            update_fields=["is_active"]
        )

        self.client.force_authenticate(
            user=self.hr_manager
        )

        response = self.client.post(
            self.activate_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_hr_manager_cannot_deactivate_department(
        self,
    ):
        self.client.force_authenticate(
            user=self.hr_manager
        )

        response = self.client.post(
            self.deactivate_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_employee_cannot_retrieve_department(self):
        self.client.force_authenticate(
            user=self.employee
        )

        response = self.client.get(
            self.detail_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_employee_cannot_update_department(self):
        self.client.force_authenticate(
            user=self.employee
        )

        response = self.client.patch(
            self.detail_url,
            {
                "name": "Unauthorized Update",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_admin_can_update_department(self):
        self.client.force_authenticate(
            user=self.admin
        )

        response = self.client.patch(
            self.detail_url,
            {
                "description": "Updated description",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            response.data["success"]
        )
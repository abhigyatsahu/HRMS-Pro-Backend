from rest_framework import status
from rest_framework.test import APITestCase

from apps.employees.models import Employee
from apps.employees.tests.factories import (
    create_branch,
    create_department,
    create_designation,
    create_employee,
    create_organization,
)
from apps.accounts.models import User

class EmployeeAPITestCase(APITestCase):

    def setUp(self):
        self.organization = create_organization(
            code="API-ORG",
            name="API Organization",
        )

        self.branch = create_branch(
            organization=self.organization,
            code="API-BR",
            name="API Branch",
        )

        self.department = create_department(
            organization=self.organization,
            code="API-DEP",
            name="API Department",
        )

        self.designation = create_designation(
            organization=self.organization,
            code="API-DES",
            name="Software Engineer",
        )

        self.user = User.objects.create_user(
            username="employee_api_admin",
            password="TestPassword123!",
            role="ADMIN",
        )

        self.client.force_authenticate(
            user=self.user
        )

        self.list_url = "/api/employees/"


    def create_employee(self, code="API001", **overrides):
        return create_employee(
            organization=self.organization,
            branch=self.branch,
            department=self.department,
            designation=self.designation,
            employee_code=code,
            **overrides,
        )

    def get_create_payload(self, **overrides):
        payload = {
            "employee_code": "NEW001",
            "first_name": "New",
            "middle_name": "",
            "last_name": "Employee",
            "date_of_birth": "1998-01-15",
            "gender": "MALE",
            "blood_group": "O+",
            "personal_email": "new@example.com",
            "work_email": "new@company.com",
            "phone": "9876543210",
            "alternate_phone": "",
            "address": "Test Address",
            "city": "Durg",
            "state": "Chhattisgarh",
            "country": "India",
            "postal_code": "491001",
            "organization": str(self.organization.uuid),
            "branch": str(self.branch.uuid),
            "department": str(self.department.uuid),
            "designation": str(self.designation.uuid),
            "joining_date": "2026-01-01",
            "confirmation_date": None,
            "employment_type": "FULL TIME",
            "employment_status": "ACTIVE",
            "reporting_manager": None,
            "is_active": True,
        }

        payload.update(overrides)

        return payload

    def test_list_employees(self):
        self.create_employee("API001")
        self.create_employee("API002")

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(response.data["success"])
        self.assertIn("items", response.data["data"])
        self.assertIn(
            "pagination",
            response.data["data"],
        )

        self.assertEqual(
            len(response.data["data"]["items"]),
            2,
        )

    def test_list_is_paginated(self):
        for index in range(1, 6):
            self.create_employee(
                f"PAGE{index:03d}"
            )

        response = self.client.get(
            f"{self.list_url}?page=1&page_size=2"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        pagination = response.data["data"]["pagination"]

        self.assertEqual(
            pagination["page"],
            1,
        )
        self.assertEqual(
            pagination["page_size"],
            2,
        )
        self.assertEqual(
            pagination["total_items"],
            5,
        )
        self.assertEqual(
            pagination["total_pages"],
            3,
        )
        self.assertTrue(
            pagination["has_next"]
        )

    def test_create_employee(self):
        response = self.client.post(
            self.list_url,
            self.get_create_payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(response.data["success"])

        self.assertEqual(
            response.data["data"]["employee_code"],
            "NEW001",
        )

        self.assertTrue(
            Employee.objects.filter(
                employee_code="NEW001"
            ).exists()
        )

    def test_create_employee_invalid_data(self):
        payload = self.get_create_payload(
            employee_code="",
            first_name="",
        )

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(response.data["success"])
        self.assertIn(
            "errors",
            response.data,
        )

    def test_retrieve_employee(self):
        employee = self.create_employee()

        url = f"{self.list_url}{employee.uuid}/"

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(response.data["success"])
        self.assertEqual(
            response.data["data"]["uuid"],
            str(employee.uuid),
        )

    def test_retrieve_nonexistent_employee(self):
        import uuid

        response = self.client.get(
            f"{self.list_url}{uuid.uuid4()}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.assertFalse(
            response.data["success"]
        )

    def test_update_employee(self):
        employee = self.create_employee()

        url = f"{self.list_url}{employee.uuid}/"

        response = self.client.patch(
            url,
            {
                "first_name": "Updated",
                "last_name": "Employee",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(response.data["success"])

        employee.refresh_from_db()

        self.assertEqual(
            employee.first_name,
            "Updated",
        )

    def test_delete_employee(self):
        employee = self.create_employee()

        url = f"{self.list_url}{employee.uuid}/"

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(response.data["success"])

        employee.refresh_from_db()

        self.assertTrue(
            employee.is_deleted
        )

        self.assertIsNotNone(
            employee.deleted_at
        )

        self.assertFalse(
            Employee.objects.filter(
                pk=employee.pk
            ).exists()
        )

    def test_deleted_employee_not_visible(self):
        employee = self.create_employee()

        employee.delete()

        response = self.client.get(self.list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        items = response.data["data"]["items"]

        returned_uuids = [
            item["uuid"]
            for item in items
        ]

        self.assertNotIn(
            str(employee.uuid),
            returned_uuids,
        )

    def test_restore_employee(self):
        employee = self.create_employee()

        employee.delete()

        url = (
            f"{self.list_url}"
            f"{employee.uuid}/restore/"
        )

        response = self.client.post(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(response.data["success"])

        employee.refresh_from_db()

        self.assertFalse(
            employee.is_deleted
        )

        self.assertIsNone(
            employee.deleted_at
        )

        self.assertTrue(
            Employee.objects.filter(
                pk=employee.pk
            ).exists()
        )

    def test_restore_active_employee_fails(self):
        employee = self.create_employee()

        response = self.client.post(
            f"{self.list_url}{employee.uuid}/restore/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(
            response.data["success"]
        )

    def test_activate_employee(self):
        employee = self.create_employee(
            "ACT001",
            is_active=False,
            employment_status="INACTIVE",
        )

        response = self.client.post(
            f"{self.list_url}"
            f"{employee.uuid}/activate/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        employee.refresh_from_db()

        self.assertTrue(
            employee.is_active
        )

        self.assertEqual(
            employee.employment_status,
            "ACTIVE",
        )

    def test_deactivate_employee(self):
        employee = self.create_employee(
            "DEACT001"
        )

        response = self.client.post(
            f"{self.list_url}"
            f"{employee.uuid}/deactivate/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        employee.refresh_from_db()

        self.assertFalse(
            employee.is_active
        )

        self.assertEqual(
            employee.employment_status,
            "INACTIVE",
        )

    def test_activate_already_active_employee_fails(self):
        employee = self.create_employee()

        response = self.client.post(
            f"{self.list_url}"
            f"{employee.uuid}/activate/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_deactivate_already_inactive_employee_fails(self):
        employee = self.create_employee(
            "INACTIVE001",
            is_active=False,
            employment_status="INACTIVE",
        )

        response = self.client.post(
            f"{self.list_url}"
            f"{employee.uuid}/deactivate/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_search_employees(self):
        self.create_employee(
            "SEARCH001",
            first_name="Rahul",
            last_name="Sharma",
        )

        self.create_employee(
            "SEARCH002",
            first_name="Amit",
            last_name="Kumar",
        )

        response = self.client.get(
            f"{self.list_url}?search=Rahul"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        items = response.data["data"]["items"]

        self.assertEqual(
            len(items),
            1,
        )

        self.assertEqual(
            items[0]["employee_code"],
            "SEARCH001",
        )

    def test_filter_by_department(self):
        employee = self.create_employee(
            "FILTER001"
        )

        response = self.client.get(
            f"{self.list_url}"
            f"?department={self.department.uuid}"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        items = response.data["data"]["items"]

        self.assertEqual(
            len(items),
            1,
        )

        self.assertEqual(
            items[0]["uuid"],
            str(employee.uuid),
        )

    def test_filter_by_active_status(self):
        self.create_employee(
            "ACTIVE001",
            is_active=True,
            employment_status="ACTIVE",
        )

        self.create_employee(
            "INACTIVE002",
            is_active=False,
            employment_status="INACTIVE",
        )

        response = self.client.get(
            f"{self.list_url}?is_active=true"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        items = response.data["data"]["items"]

        self.assertEqual(
            len(items),
            1,
        )

        self.assertEqual(
            items[0]["employee_code"],
            "ACTIVE001",
        )
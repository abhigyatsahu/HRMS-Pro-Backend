from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.designations.models import Designation
from apps.organization.models import Organization


class DesignationAPITests(APITestCase):
    """
    API tests for the Designation module.
    """

    @classmethod
    def setUpTestData(cls):
        cls.organization = Organization.objects.create(
            name="ABC Technologies",
            code="ABC",
            legal_name="ABC Technologies Pvt Ltd",
            email="admin@abc.com",
            phone="9876543210",
            city="Raipur",
            state="Chhattisgarh",
            country="India",
            postal_code="492001",
            is_active=True,
        )

        cls.organization_2 = Organization.objects.create(
            name="XYZ Technologies",
            code="XYZ",
            legal_name="XYZ Technologies Pvt Ltd",
            email="admin@xyz.com",
            phone="9876543211",
            city="Bhilai",
            state="Chhattisgarh",
            country="India",
            postal_code="490001",
            is_active=True,
        )

    def setUp(self):
        self.super_admin = User.objects.create_user(
            username="superadmin",
            email="superadmin@test.com",
            password="Test@12345",
            role=User.Role.SUPER_ADMIN,
            is_active=True,
        )

        self.admin = User.objects.create_user(
            username="admin",
            email="admin@test.com",
            password="Test@12345",
            role=User.Role.ADMIN,
            is_active=True,
        )

        self.hr_manager = User.objects.create_user(
            username="hrmanager",
            email="hr@test.com",
            password="Test@12345",
            role=User.Role.HR_MANAGER,
            is_active=True,
        )

        self.manager = User.objects.create_user(
            username="manager",
            email="manager@test.com",
            password="Test@12345",
            role=User.Role.MANAGER,
            is_active=True,
        )

        self.employee = User.objects.create_user(
            username="employee",
            email="employee@test.com",
            password="Test@12345",
            role=User.Role.EMPLOYEE,
            is_active=True,
        )

        self.designation = Designation.objects.create(
            organization=self.organization,
            name="Software Engineer",
            code="SE",
            description="Software development role",
            level=2,
            is_active=True,
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def authenticate(self, user):
        """
        Authenticate using the project's normal DRF authentication.
        """
        self.client.force_authenticate(user=user)

    def list_url(self):
        return reverse(
            "designation-list-create"
        )

    def detail_url(self, uuid):
        return reverse(
            "designation-detail",
            kwargs={"uuid": uuid},
        )

    def activate_url(self, uuid):
        return reverse(
            "designation-activate",
            kwargs={"uuid": uuid},
        )

    def deactivate_url(self, uuid):
        return reverse(
            "designation-deactivate",
            kwargs={"uuid": uuid},
        )

    def delete_url(self, uuid):
        return reverse(
            "designation-delete",
            kwargs={"uuid": uuid},
        )

    def restore_url(self, uuid):
        return reverse(
            "designation-restore",
            kwargs={"uuid": uuid},
        )

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def test_list_requires_authentication(self):
        response = self.client.get(
            self.list_url()
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_create_requires_authentication(self):
        response = self.client.post(
            self.list_url(),
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    # ------------------------------------------------------------------
    # List permissions
    # ------------------------------------------------------------------

    def test_super_admin_can_list(self):
        self.authenticate(self.super_admin)

        response = self.client.get(
            self.list_url()
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_admin_can_list(self):
        self.authenticate(self.admin)

        response = self.client.get(
            self.list_url()
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_hr_manager_can_list(self):
        self.authenticate(self.hr_manager)

        response = self.client.get(
            self.list_url()
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_manager_can_list(self):
        self.authenticate(self.manager)

        response = self.client.get(
            self.list_url()
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_employee_cannot_list(self):
        self.authenticate(self.employee)

        response = self.client.get(
            self.list_url()
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    # ------------------------------------------------------------------
    # List
    # ------------------------------------------------------------------

    def test_list_designations(self):
        self.authenticate(self.admin)

        response = self.client.get(
            self.list_url()
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertTrue(response.data["success"])

        self.assertEqual(
            response.data["message"],
            "Data fetched successfully.",
        )

        items = response.data["data"]["items"]

        self.assertEqual(
            len(items),
            1,
        )

        self.assertEqual(
            items[0]["code"],
            "SE",
        )

        self.assertEqual(
            items[0]["name"],
            self.designation.name,
        )

    # ------------------------------------------------------------------
    # Create permissions
    # ------------------------------------------------------------------

    def test_super_admin_can_create(self):
        self.authenticate(self.super_admin)

        response = self.client.post(
            self.list_url(),
            {
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "Project Manager",
                "code": "PM",
                "description": "Project management role",
                "level": 3,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_admin_can_create(self):
        self.authenticate(self.admin)

        response = self.client.post(
            self.list_url(),
            {
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "Team Lead",
                "code": "TL",
                "description": "Team lead role",
                "level": 3,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_hr_manager_can_create(self):
        self.authenticate(self.hr_manager)

        response = self.client.post(
            self.list_url(),
            {
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "HR Executive",
                "code": "HRE",
                "description": "HR role",
                "level": 2,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_manager_cannot_create(self):
        self.authenticate(self.manager)

        response = self.client.post(
            self.list_url(),
            {
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "Manager",
                "code": "MGR",
                "description": "Manager role",
                "level": 3,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_employee_cannot_create(self):
        self.authenticate(self.employee)

        response = self.client.post(
            self.list_url(),
            {
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "Employee",
                "code": "EMP",
                "description": "Employee role",
                "level": 1,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    # ------------------------------------------------------------------
    # Create
    # ------------------------------------------------------------------

    def test_create_designation(self):
        self.authenticate(self.admin)

        response = self.client.post(
            self.list_url(),
            {
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "Backend Developer",
                "code": "BE",
                "description": "Backend development",
                "level": 2,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["message"],
            "Designation created successfully.",
        )

        self.assertEqual(
            response.data["data"]["name"],
            "Backend Developer",
        )

        self.assertEqual(
            response.data["data"]["code"],
            "BE",
        )

    def test_duplicate_designation_code_returns_409(self):
        self.authenticate(self.admin)

        response = self.client.post(
            self.list_url(),
            {
                "organization_uuid": str(
                    self.organization.uuid
                ),
                "name": "Another Software Engineer",
                "code": "SE",
                "description": "Duplicate code",
                "level": 2,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_409_CONFLICT,
        )

    def test_same_code_allowed_for_different_organization(self):
        self.authenticate(self.admin)

        response = self.client.post(
            self.list_url(),
            {
                "organization_uuid": str(
                    self.organization_2.uuid
                ),
                "name": "Software Engineer",
                "code": "SE",
                "description": "Same code in another organization",
                "level": 2,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    # ------------------------------------------------------------------
    # Retrieve
    # ------------------------------------------------------------------

    def test_retrieve_designation(self):
        self.authenticate(self.admin)

        response = self.client.get(
            self.detail_url(
                self.designation.uuid
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["message"],
            "Designation retrieved successfully.",
        )

        self.assertEqual(
            response.data["data"]["name"],
            "Software Engineer",
        )

    def test_retrieve_nonexistent_designation_returns_404(self):
        self.authenticate(self.admin)

        import uuid

        response = self.client.get(
            self.detail_url(uuid.uuid4())
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def test_admin_can_update(self):
        self.authenticate(self.admin)

        response = self.client.patch(
            self.detail_url(
                self.designation.uuid
            ),
            {
                "name": "Senior Software Engineer",
                "level": 3,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["message"],
            "Designation updated successfully.",
        )

        self.designation.refresh_from_db()

        self.assertEqual(
            self.designation.name,
            "Senior Software Engineer",
        )

        self.assertEqual(
            self.designation.level,
            3,
        )

    def test_hr_manager_can_update(self):
        self.authenticate(self.hr_manager)

        response = self.client.patch(
            self.detail_url(
                self.designation.uuid
            ),
            {
                "description": "Updated description",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_manager_cannot_update(self):
        self.authenticate(self.manager)

        response = self.client.patch(
            self.detail_url(
                self.designation.uuid
            ),
            {
                "name": "Unauthorized Update",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_employee_cannot_update(self):
        self.authenticate(self.employee)

        response = self.client.patch(
            self.detail_url(
                self.designation.uuid
            ),
            {
                "name": "Unauthorized Update",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    # ------------------------------------------------------------------
    # Activate / Deactivate
    # ------------------------------------------------------------------

    def test_admin_can_deactivate(self):
        self.authenticate(self.admin)

        response = self.client.post(
            self.deactivate_url(
                self.designation.uuid
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["message"],
            "Designation deactivated successfully.",
        )

        self.designation.refresh_from_db()

        self.assertFalse(
            self.designation.is_active
        )

    def test_admin_can_activate(self):
        self.designation.is_active = False
        self.designation.save(
            update_fields=["is_active"]
        )

        self.authenticate(self.admin)

        response = self.client.post(
            self.activate_url(
                self.designation.uuid
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["message"],
            "Designation activated successfully.",
        )

        self.designation.refresh_from_db()

        self.assertTrue(
            self.designation.is_active
        )

    def test_manager_cannot_activate(self):
        self.authenticate(self.manager)

        response = self.client.post(
            self.activate_url(
                self.designation.uuid
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_manager_cannot_deactivate(self):
        self.authenticate(self.manager)

        response = self.client.post(
            self.deactivate_url(
                self.designation.uuid
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    # ------------------------------------------------------------------
    # Soft Delete
    # ------------------------------------------------------------------

    def test_admin_can_soft_delete(self):
        self.authenticate(self.admin)

        response = self.client.delete(
            self.delete_url(
                self.designation.uuid
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["message"],
            "Designation deleted successfully.",
        )

        self.designation.refresh_from_db()

        self.assertTrue(
            self.designation.is_deleted
        )

    def test_soft_deleted_designation_is_not_in_normal_queryset(self):
        self.designation.delete()

        self.assertFalse(
            Designation.objects.filter(
                uuid=self.designation.uuid
            ).exists()
        )

    def test_soft_deleted_designation_remains_in_all_objects(self):
        self.designation.delete()

        self.assertTrue(
            Designation.all_objects.filter(
                uuid=self.designation.uuid
            ).exists()
        )

    def test_deleted_designation_cannot_be_retrieved(self):
        self.designation.delete()

        self.authenticate(self.admin)

        response = self.client.get(
            self.detail_url(
                self.designation.uuid
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    # ------------------------------------------------------------------
    # Restore
    # ------------------------------------------------------------------

    def test_admin_can_restore_designation(self):
        self.designation.delete()

        self.authenticate(self.admin)

        response = self.client.post(
            self.restore_url(
                self.designation.uuid
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["message"],
            "Designation restored successfully.",
        )

        self.designation.refresh_from_db()

        self.assertFalse(
            self.designation.is_deleted
        )

        self.assertTrue(
            Designation.objects.filter(
                uuid=self.designation.uuid
            ).exists()
        )

    def test_manager_cannot_restore_designation(self):
        self.designation.delete()

        self.authenticate(self.manager)

        response = self.client.post(
            self.restore_url(
                self.designation.uuid
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    # ------------------------------------------------------------------
    # Delete permissions
    # ------------------------------------------------------------------

    def test_manager_cannot_delete(self):
        self.authenticate(self.manager)

        response = self.client.delete(
            self.delete_url(
                self.designation.uuid
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_employee_cannot_delete(self):
        self.authenticate(self.employee)

        response = self.client.delete(
            self.delete_url(
                self.designation.uuid
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def test_search_by_name(self):
        self.authenticate(self.admin)

        response = self.client.get(
            self.list_url(),
            {
                "search": "Software",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        items = response.data["data"]["items"]
        names = [
            item["name"]
            for item in items
        ]

        self.assertIn(
            "Software Engineer",
            names,
        )

        # print("\nRESPONSE:")
        # print(response.data)

    def test_search_by_code(self):
        self.authenticate(self.admin)

        response = self.client.get(
            self.list_url(),
            {
                "search": "SE",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        items = response.data["data"]["items"]
        codes = [
            item["code"]
            for item in items
        ]

        self.assertIn(
            "SE",
            codes,
        )

        # print("\nRESPONSE:")
        # print(response.data)

    def test_search_by_description(self):
        self.authenticate(self.admin)

        response = self.client.get(
            self.list_url(),
            {
                "search": "development",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        descriptions = [
            item["description"]
            for item in response.data["data"]["items"]
        ]

        self.assertTrue(
            any(
                "development" in description.lower()
                for description in descriptions
            )
        )

        # print("\nRESPONSE:")
        # print(response.data)

    # ------------------------------------------------------------------
    # Ordering
    # ------------------------------------------------------------------

    def test_ordering_by_name(self):
        Designation.objects.create(
            organization=self.organization,
            name="Accountant",
            code="ACC",
            description="Finance role",
            level=1,
            is_active=True,
        )

        self.authenticate(self.admin)

        response = self.client.get(
            self.list_url(),
            {
                "ordering": "name",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        data = response.data["data"]

        if isinstance(data, dict):
            results = data.get("items", data.get("results", data))
        else:
            results = data

        names = [
            item["name"]
            for item in results
        ]

        self.assertEqual(
            names,
            sorted(names),
        )

        # print("\nRESPONSE:")
        # print(response.data)

    # ------------------------------------------------------------------
    # Pagination
    # ------------------------------------------------------------------

    def test_pagination(self):
        for index in range(5):
            Designation.objects.create(
                organization=self.organization,
                name=f"Designation {index}",
                code=f"D{index}",
                description="Test designation",
                level=1,
                is_active=True,
            )

        self.authenticate(self.admin)

        response = self.client.get(
            self.list_url(),
            {
                "page": 1,
                "page_size": 2,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def get_response_items(self, response):
        """
        Extract list items from both paginated
        and non-paginated API responses.
        """
        data = response.data["data"]

        if isinstance(data, dict):
            return data.get(
                "results",
                []
            )

        return data
from django.test import TestCase
from rest_framework.test import APIClient
from apps.accounts.models import User
from apps.organization.models import Organization, Branch
from .factories import create_organization, create_branch

class SoftDeleteTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.admin = User.objects.create_user(
            username="admin_sd",
            email="admin_sd@test.com",
            password="Admin@123_sd",
            role=User.Role.ADMIN,
        )
        self.client.force_authenticate(user=self.admin)

    def test_soft_delete_defaults(self):
        # 1. New model defaults to is_deleted=False
        org = create_organization(name="SD Org", code="SDO")
        self.assertFalse(org.is_deleted)

    def test_soft_delete_instance_delete(self):
        # 2. Calling instance.delete() does not remove the row from DB but sets is_deleted=True
        org = create_organization(name="SD Org 2", code="SD2")
        pk = org.pk
        
        # Call delete
        deleted_count, details = org.delete()
        
        # Verify returned count
        self.assertEqual(deleted_count, 1)
        
        # Check that it's marked as deleted
        org.refresh_from_db()
        self.assertTrue(org.is_deleted)
        
        # Verify it still exists in the DB (using all_objects)
        self.assertTrue(Organization.all_objects.filter(pk=pk).exists())
        # Verify it is not found by the default objects manager
        self.assertFalse(Organization.objects.filter(pk=pk).exists())

    def test_soft_delete_queryset_bulk_delete(self):
        # 6. QuerySet.delete() performs soft deletion
        org1 = create_organization(name="Bulk 1", code="B1")
        org2 = create_organization(name="Bulk 2", code="B2")
        
        # Bulk delete
        queryset = Organization.objects.filter(code__in=["B1", "B2"])
        deleted_count, details = queryset.delete()
        
        self.assertEqual(deleted_count, 2)
        
        org1.refresh_from_db()
        org2.refresh_from_db()
        self.assertTrue(org1.is_deleted)
        self.assertTrue(org2.is_deleted)
        
        self.assertEqual(Organization.objects.filter(code__in=["B1", "B2"]).count(), 0)
        self.assertEqual(Organization.all_objects.filter(code__in=["B1", "B2"]).count(), 2)

    def test_soft_delete_api_endpoints(self):
        # 7. Deleted records do not appear in normal list APIs
        # 9. Deleted records cannot be retrieved through normal detail APIs
        org = create_organization(name="API Soft Delete", code="ASD")
        
        # Verify it shows up in list API initially
        response = self.client.get("/api/v1/organizations/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(item["uuid"] == str(org.uuid) for item in response.data["data"]["items"]))
        
        # Verify retrieve works
        response = self.client.get(f"/api/v1/organizations/{org.uuid}/")
        self.assertEqual(response.status_code, 200)
        
        # Soft delete the organization
        org.delete()
        
        # Verify it NO LONGER shows up in list API
        response = self.client.get("/api/v1/organizations/")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(any(item["uuid"] == str(org.uuid) for item in response.data["data"]["items"]))
        
        # Verify retrieve returns 404
        response = self.client.get(f"/api/v1/organizations/{org.uuid}/")
        self.assertEqual(response.status_code, 404)

    def test_soft_delete_search(self):
        # 8. Deleted records do not appear in normal search
        org = create_organization(name="Search SD", code="SSD")
        
        # Verify search returns it
        response = self.client.get("/api/v1/organizations/?search=SSD")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(item["uuid"] == str(org.uuid) for item in response.data["data"]["items"]))
        
        # Soft delete
        org.delete()
        
        # Verify search does NOT return it
        response = self.client.get("/api/v1/organizations/?search=SSD")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(any(item["uuid"] == str(org.uuid) for item in response.data["data"]["items"]))

    def test_organization_isolation(self):
        # 10. Organization/tenant isolation remains intact with soft deletes
        org_a = create_organization(name="Org A", code="OGA")
        org_b = create_organization(name="Org B", code="OGB")
        
        branch_a1 = create_branch(org_a, name="Branch A1", code="BRA1")
        branch_a2 = create_branch(org_a, name="Branch A2", code="BRA2")
        branch_b1 = create_branch(org_b, name="Branch B1", code="BRB1")
        
        # Soft delete branch A2
        branch_a2.delete()
        
        # Query active branches for Org A
        active_org_a_branches = Branch.objects.filter(organization=org_a)
        self.assertEqual(active_org_a_branches.count(), 1)
        self.assertEqual(active_org_a_branches.first().pk, branch_a1.pk)
        
        # Query all branches including deleted for Org A
        all_org_a_branches = Branch.all_objects.filter(organization=org_a)
        self.assertEqual(all_org_a_branches.count(), 2)

    def test_unique_constraints(self):
        # 11. Existing unique constraints continue to behave exactly as defined
        org = create_organization(name="Unique Test Org", code="UTO")
        create_branch(org, name="Branch U1", code="BRU1")
        
        # Creating another branch with same code for same org should fail
        with self.assertRaises(Exception):
            create_branch(org, name="Branch U2", code="BRU1")

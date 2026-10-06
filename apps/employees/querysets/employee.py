from apps.core.querysets.soft_delete import SoftDeleteQuerySet
from django.db import models

class EmployeeQuerySet(SoftDeleteQuerySet):

    def active(self):
        return self.filter(
            is_active=True,
            employment_status="ACTIVE",
        )

    def inactive(self):
        return self.filter(
            is_active=False,
        )

    def for_organization(self, organization):
        return self.filter(
            organization=organization,
        )

    def for_branch(self, branch):
        return self.filter(
            branch=branch,
        )

    def for_department(self, department):
        return self.filter(
            department=department,
        )

    def for_designation(self, designation):
        return self.filter(
            designation=designation,
        )

    def search(self, value):
        if not value:
            return self

        value = value.strip()

        if not value:
            return self

        return self.filter(
            models.Q(employee_code__icontains=value)
            | models.Q(first_name__icontains=value)
            | models.Q(middle_name__icontains=value)
            | models.Q(last_name__icontains=value)
            | models.Q(work_email__icontains=value)
            | models.Q(personal_email__icontains=value)
            | models.Q(phone__icontains=value)
        )
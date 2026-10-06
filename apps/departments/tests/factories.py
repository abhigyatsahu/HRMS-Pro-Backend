from apps.departments.models import Department
from apps.organization.models import Organization


def create_organization(
    *,
    name="Test Organization",
    code="TEST",
    is_active=True,
):
    return Organization.objects.create(
        name=name,
        code=code,
        is_active=is_active,
    )


def create_department(
    *,
    organization,
    name="Human Resources",
    code="HR",
    description="Human Resources Department",
    is_active=True,
):
    return Department.objects.create(
        organization=organization,
        name=name,
        code=code,
        description=description,
        is_active=is_active,
    )
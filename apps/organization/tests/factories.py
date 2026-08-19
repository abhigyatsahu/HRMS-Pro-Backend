from apps.organization.models import Organization


def create_organization(
    *,
    name="ABC Technologies",
    code="ABC",
    email="admin@abc.com",
    is_active=True,
):
    return Organization.objects.create(
        name=name,
        code=code,
        email=email,
        is_active=is_active,
    )
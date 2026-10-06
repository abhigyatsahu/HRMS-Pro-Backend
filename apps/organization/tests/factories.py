import uuid

from apps.accounts.models import User
from apps.organization.models import (
    Branch,
    Organization,
)


def create_user(
    *,
    email="admin@test.com",
    role=User.Role.ADMIN,
):
    return User.objects.create_user(
        username=email,
        email=email,
        password="TestPassword123!",
        role=role,
        is_active=True,
    )


def create_organization(
    *,
    name="ABC Technologies",
    code="ABC",
    legal_name="ABC Technologies Pvt Ltd",
    email="contact@abc.com",
    phone="9876543210",
    website="https://abc.com",
    address="Test Address",
    city="Raipur",
    state="Chhattisgarh",
    country="India",
    postal_code="492001",
    is_active=True,
):
    return Organization.objects.create(
        name=name,
        code=code,
        legal_name=legal_name,
        email=email,
        phone=phone,
        website=website,
        address=address,
        city=city,
        state=state,
        country=country,
        postal_code=postal_code,
        is_active=is_active,
    )


def create_branch(
    organization,
    *,
    name="Test Branch",
    code="BR001",
    is_active=True,
):
    return Branch.objects.create(
        organization=organization,
        name=name,
        code=code,
        is_active=is_active,
    )
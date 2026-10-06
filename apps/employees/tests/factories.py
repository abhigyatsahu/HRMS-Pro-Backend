from apps.departments.models import Department
from apps.designations.models import Designation
from apps.employees.models import Employee
from apps.organization.models import Branch, Organization
from datetime import date

def create_organization(
    code="TEST-ORG",
    name="Test Organization",
):
    return Organization.objects.create(
        code=code,
        name=name,
    )


def create_branch(
    organization,
    code="TEST-BR",
    name="Test Branch",
):
    return Branch.objects.create(
        organization=organization,
        code=code,
        name=name,
    )


def create_department(
    organization,
    code="TEST-DEP",
    name="Test Department",
):
    return Department.objects.create(
        organization=organization,
        code=code,
        name=name,
    )


def create_designation(
    organization,
    code="TEST-DES",
    name="Test Designation",
    level=1,
):
    return Designation.objects.create(
        organization=organization,
        code=code,
        name=name,
        level=level,
    )


def create_employee(
    organization,
    branch,
    department,
    designation,
    employee_code="TEST001",
    first_name="Test",
    middle_name="",
    last_name="Employee",
    **overrides,
):
    defaults = {
        "employee_code": employee_code,
        "first_name": first_name,
        "middle_name": middle_name,
        "last_name": last_name,
        "date_of_birth": None,
        "gender": "",
        "blood_group": "",
        "personal_email": "",
        "work_email": "",
        "phone": "",
        "alternate_phone": "",
        "address": "",
        "city": "",
        "state": "",
        "country": "India",
        "postal_code": "",
        "organization": organization,
        "branch": branch,
        "department": department,
        "designation": designation,
        "joining_date": date(2026, 1, 1),
        "confirmation_date": None,
        "employment_type": "FULL TIME",
        "employment_status": "ACTIVE",
        "reporting_manager": None,
        "is_active": True,
    }

    defaults.update(overrides)

    return Employee.objects.create(**defaults)
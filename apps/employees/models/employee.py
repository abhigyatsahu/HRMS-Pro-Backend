import uuid
from apps.employees.managers.employee import EmployeeManager
from apps.employees.querysets.employee import EmployeeQuerySet
from django.db import models

from apps.common.choices.blood_group import BloodGroupType
from apps.common.choices.employment import EmploymentTypeChoices
from apps.common.choices.gender import GenderChoices
from apps.common.choices.status import StatusChoices
from apps.core.models.soft_delete import SoftDeleteModel
from apps.organization.models import Organization, Branch
from apps.departments.models import Department
from apps.designations.models import Designation


class Employee(SoftDeleteModel):
    objects = EmployeeManager()
    all_objects = models.Manager.from_queryset(EmployeeQuerySet)()
    # -------------------------------------------------------------------------
    # Identity
    # -------------------------------------------------------------------------


    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    employee_code = models.CharField(
        max_length=50,
        unique=True,
    )

    first_name = models.CharField(
        max_length=100,
    )

    middle_name = models.CharField(
        max_length=100,
        blank=True,
    )

    last_name = models.CharField(
        max_length=100,
        blank=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    gender = models.CharField(
        max_length=20,
        choices=GenderChoices.choices,
        blank=True,
    )

    blood_group = models.CharField(
        max_length=5,
        choices=BloodGroupType.choices,
        blank=True,
    )

    profile_photo = models.ImageField(
        upload_to="employees/profile_photos/",
        blank=True,
        null=True,
    )

    # -------------------------------------------------------------------------
    # Contact
    # -------------------------------------------------------------------------

    personal_email = models.EmailField(
        blank=True,
    )

    work_email = models.EmailField(
        blank=True,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    alternate_phone = models.CharField(
        max_length=20,
        blank=True,
    )

    address = models.TextField(
        blank=True,
    )

    city = models.CharField(
        max_length=100,
        blank=True,
    )

    state = models.CharField(
        max_length=100,
        blank=True,
    )

    country = models.CharField(
        max_length=100,
        default="India",
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
    )

    # -------------------------------------------------------------------------
    # Organization
    # -------------------------------------------------------------------------

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="employees",
    )

    branch = models.ForeignKey(
        Branch,
        on_delete=models.PROTECT,
        related_name="employees",
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="employees",
    )

    designation = models.ForeignKey(
        Designation,
        on_delete=models.PROTECT,
        related_name="employees",
    )

    # -------------------------------------------------------------------------
    # Employment
    # -------------------------------------------------------------------------

    joining_date = models.DateField()

    confirmation_date = models.DateField(
        null=True,
        blank=True,
    )

    employment_type = models.CharField(
        max_length=30,
        choices=EmploymentTypeChoices.choices,
    )

    employment_status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
        db_index=True,
    )

    reporting_manager = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="subordinates",
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    # -------------------------------------------------------------------------
    # Audit
    # -------------------------------------------------------------------------

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        app_label = "employees"
        db_table = "employees"
        ordering = ["employee_code"]
        indexes = [
            models.Index(
                fields=["organization", "is_active"],
                name="employee_org_active_idx",
            ),
            models.Index(
                fields=["organization", "department"],
                name="employee_org_dept_idx",
            ),
            models.Index(
                fields=["organization", "branch"],
                name="employee_org_branch_idx",
            ),
            models.Index(
                fields=["organization", "designation"],
                name="employee_org_desig_idx",
            ),
            models.Index(
                fields=["employment_status"],
                name="employee_status_idx",
            ),
        ]

    def __str__(self):
        return f"{self.employee_code} - {self.full_name}"

    @property
    def full_name(self):
        return " ".join(
            part
            for part in [
                self.first_name,
                self.middle_name,
                self.last_name,
            ]
            if part
        )
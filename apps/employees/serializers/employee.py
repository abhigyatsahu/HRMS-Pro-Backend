from rest_framework import serializers

from apps.departments.models import Department
from apps.designations.models import Designation
from apps.employees.models import Employee
from apps.organization.models import Branch, Organization


class OrganizationNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "uuid",
            "name",
        ]


class BranchNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = [
            "uuid",
            "name",
        ]


class DepartmentNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "uuid",
            "name",
        ]


class DesignationNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = [
            "uuid",
            "name",
            "code",
            "level",
        ]


class ReportingManagerNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            "uuid",
            "employee_code",
            "full_name",
        ]


class EmployeeSerializer(serializers.ModelSerializer):
    organization = OrganizationNestedSerializer(read_only=True)
    branch = BranchNestedSerializer(read_only=True)
    department = DepartmentNestedSerializer(read_only=True)
    designation = DesignationNestedSerializer(read_only=True)
    reporting_manager = ReportingManagerNestedSerializer(read_only=True)

    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Employee
        fields = [
            "uuid",
            "employee_code",
            "first_name",
            "middle_name",
            "last_name",
            "full_name",
            "date_of_birth",
            "gender",
            "blood_group",
            "profile_photo",
            "personal_email",
            "work_email",
            "phone",
            "alternate_phone",
            "address",
            "city",
            "state",
            "country",
            "postal_code",
            "organization",
            "branch",
            "department",
            "designation",
            "joining_date",
            "confirmation_date",
            "employment_type",
            "employment_status",
            "reporting_manager",
            "is_active",
            "is_deleted",
            "deleted_at",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "uuid",
            "full_name",
            "is_deleted",
            "deleted_at",
            "created_at",
            "updated_at",
        ]


class EmployeeCreateSerializer(serializers.ModelSerializer):
    organization = serializers.UUIDField()
    branch = serializers.UUIDField()
    department = serializers.UUIDField()
    designation = serializers.UUIDField()
    reporting_manager = serializers.UUIDField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Employee
        fields = [
            "employee_code",
            "first_name",
            "middle_name",
            "last_name",
            "date_of_birth",
            "gender",
            "blood_group",
            "profile_photo",
            "personal_email",
            "work_email",
            "phone",
            "alternate_phone",
            "address",
            "city",
            "state",
            "country",
            "postal_code",
            "organization",
            "branch",
            "department",
            "designation",
            "joining_date",
            "confirmation_date",
            "employment_type",
            "employment_status",
            "reporting_manager",
            "is_active",
        ]

    def validate_organization(self, value):
        try:
            return Organization.objects.get(uuid=value)
        except Organization.DoesNotExist:
            raise serializers.ValidationError(
                "Organization does not exist."
            )

    def validate_branch(self, value):
        try:
            return Branch.objects.get(uuid=value)
        except Branch.DoesNotExist:
            raise serializers.ValidationError(
                "Branch does not exist."
            )

    def validate_department(self, value):
        try:
            return Department.objects.get(uuid=value)
        except Department.DoesNotExist:
            raise serializers.ValidationError(
                "Department does not exist."
            )

    def validate_designation(self, value):
        try:
            return Designation.objects.get(uuid=value)
        except Designation.DoesNotExist:
            raise serializers.ValidationError(
                "Designation does not exist."
            )

    def validate_reporting_manager(self, value):
        if value is None:
            return None

        try:
            return Employee.objects.get(uuid=value)
        except Employee.DoesNotExist:
            raise serializers.ValidationError(
                "Reporting manager does not exist."
            )

    def validate(self, attrs):
        organization = attrs["organization"]

        for field in [
            "branch",
            "department",
            "designation",
        ]:
            related_object = attrs[field]

            if related_object.organization_id != organization.id:
                raise serializers.ValidationError({
                    field: (
                        f"{field.capitalize()} does not belong "
                        "to the selected organization."
                    )
                })

        reporting_manager = attrs.get("reporting_manager")

        if reporting_manager and reporting_manager.organization_id != organization.id:
            raise serializers.ValidationError({
                "reporting_manager": (
                    "Reporting manager does not belong "
                    "to the selected organization."
                )
            })

        return attrs


class EmployeeUpdateSerializer(serializers.ModelSerializer):
    organization = serializers.UUIDField(required=False)
    branch = serializers.UUIDField(required=False)
    department = serializers.UUIDField(required=False)
    designation = serializers.UUIDField(required=False)
    reporting_manager = serializers.UUIDField(
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Employee
        fields = [
            "employee_code",
            "first_name",
            "middle_name",
            "last_name",
            "date_of_birth",
            "gender",
            "blood_group",
            "profile_photo",
            "personal_email",
            "work_email",
            "phone",
            "alternate_phone",
            "address",
            "city",
            "state",
            "country",
            "postal_code",
            "organization",
            "branch",
            "department",
            "designation",
            "joining_date",
            "confirmation_date",
            "employment_type",
            "employment_status",
            "reporting_manager",
            "is_active",
        ]

    def _get_organization(self, value):
        try:
            return Organization.objects.get(uuid=value)
        except Organization.DoesNotExist:
            raise serializers.ValidationError(
                "Organization does not exist."
            )

    def _get_branch(self, value):
        try:
            return Branch.objects.get(uuid=value)
        except Branch.DoesNotExist:
            raise serializers.ValidationError(
                "Branch does not exist."
            )

    def _get_department(self, value):
        try:
            return Department.objects.get(uuid=value)
        except Department.DoesNotExist:
            raise serializers.ValidationError(
                "Department does not exist."
            )

    def _get_designation(self, value):
        try:
            return Designation.objects.get(uuid=value)
        except Designation.DoesNotExist:
            raise serializers.ValidationError(
                "Designation does not exist."
            )

    def _get_reporting_manager(self, value):
        if value is None:
            return None

        try:
            return Employee.objects.get(uuid=value)
        except Employee.DoesNotExist:
            raise serializers.ValidationError(
                "Reporting manager does not exist."
            )

    def validate_organization(self, value):
        return self._get_organization(value)

    def validate_branch(self, value):
        return self._get_branch(value)

    def validate_department(self, value):
        return self._get_department(value)

    def validate_designation(self, value):
        return self._get_designation(value)

    def validate_reporting_manager(self, value):
        manager = self._get_reporting_manager(value)

        if self.instance and manager.pk == self.instance.pk:
            raise serializers.ValidationError(
                "An employee cannot be their own reporting manager."
            )

        return manager

    def validate(self, attrs):
        organization = attrs.get(
            "organization",
            self.instance.organization,
        )

        for field in [
            "branch",
            "department",
            "designation",
        ]:
            related_object = attrs.get(
                field,
                getattr(self.instance, field),
            )

            if related_object.organization_id != organization.id:
                raise serializers.ValidationError({
                    field: (
                        f"{field.capitalize()} does not belong "
                        "to the selected organization."
                    )
                })

        reporting_manager = attrs.get(
            "reporting_manager",
            self.instance.reporting_manager,
        )

        if (
            reporting_manager
            and reporting_manager.organization_id != organization.id
        ):
            raise serializers.ValidationError({
                "reporting_manager": (
                    "Reporting manager does not belong "
                    "to the selected organization."
                )
            })

        return attrs
from apps.accounts.models import User

from .base import RolePermission


class OrganizationReadPermission(RolePermission):
    """
    Permission for viewing organizations.
    """

    allowed_roles = {
        User.Role.SUPER_ADMIN,
        User.Role.ADMIN,
        User.Role.HR_MANAGER,
    }


class OrganizationManagePermission(RolePermission):
    """
    Permission for creating and updating organizations.
    """

    allowed_roles = {
        User.Role.SUPER_ADMIN,
        User.Role.ADMIN,
    }


class OrganizationStatusPermission(RolePermission):
    """
    Permission for activating/deactivating organizations.
    """

    allowed_roles = {
        User.Role.SUPER_ADMIN,
        User.Role.ADMIN,
    }
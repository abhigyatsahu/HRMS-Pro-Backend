from apps.accounts.models import User

from .base import RolePermission


class DesignationReadPermission(RolePermission):
    """
    Permission for viewing designations.
    """

    allowed_roles = {
        User.Role.SUPER_ADMIN,
        User.Role.ADMIN,
        User.Role.HR_MANAGER,
        User.Role.MANAGER,
    }


class DesignationManagePermission(RolePermission):
    """
    Permission for creating and updating designations.
    """

    allowed_roles = {
        User.Role.SUPER_ADMIN,
        User.Role.ADMIN,
        User.Role.HR_MANAGER,
    }


class DesignationStatusPermission(RolePermission):
    """
    Permission for activating/deactivating designations.
    """

    allowed_roles = {
        User.Role.SUPER_ADMIN,
        User.Role.ADMIN,
        User.Role.HR_MANAGER,
    }


class DesignationDeletePermission(RolePermission):
    """
    Permission for soft-deleting designations.
    """

    allowed_roles = {
        User.Role.SUPER_ADMIN,
        User.Role.ADMIN,
    }
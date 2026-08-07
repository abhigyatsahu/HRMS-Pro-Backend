from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    def has_permission(
        self,
        request,
        view,
    ):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "SUPER_ADMIN"
        )


class IsAdminOrSuperAdmin(BasePermission):
    allowed_roles = {
        "SUPER_ADMIN",
        "ADMIN",
    }

    def has_permission(
        self,
        request,
        view,
    ):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role
            in self.allowed_roles
        )


class IsHR(BasePermission):
    allowed_roles = {
        "SUPER_ADMIN",
        "ADMIN",
        "HR_MANAGER",
    }

    def has_permission(
        self,
        request,
        view,
    ):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role
            in self.allowed_roles
        )
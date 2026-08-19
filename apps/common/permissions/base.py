from rest_framework.permissions import BasePermission


class RolePermission(BasePermission):
    """
    Base permission class for role-based access control.
    """

    allowed_roles = set()

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return user.role in self.allowed_roles
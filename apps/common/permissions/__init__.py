from .base import RolePermission
from .organization import (
    OrganizationManagePermission,
    OrganizationReadPermission,
    OrganizationStatusPermission,
)
from .designation import (
    DesignationReadPermission,
    DesignationManagePermission,
    DesignationStatusPermission,
    DesignationDeletePermission,
)


__all__ = [
    "RolePermission",
    "OrganizationReadPermission",
    "OrganizationManagePermission",
    "OrganizationStatusPermission",
    "DesignationReadPermission",
    "DesignationManagePermission",
    "DesignationStatusPermission",
    "DesignationDeletePermission",
]
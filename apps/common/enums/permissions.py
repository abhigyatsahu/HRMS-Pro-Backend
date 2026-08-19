from .base import BaseEnum

class PermissionAction(BaseEnum):
    """
    Actions that can be performed against a resource.
    """

    VIEW = "view"

    CREATE = "create"

    UPDATE = "update"

    DELETE = "delete"

    APPROVE = "approve"

    REJECT = "reject"
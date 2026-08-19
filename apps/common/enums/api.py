from .base import BaseEnum

class APIAction(BaseEnum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
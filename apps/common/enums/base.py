from enum import Enum


class BaseEnum(str, Enum):
    """
    Base enum for application-level string enums.
    """

    def __str__(self) -> str:
        return self.value
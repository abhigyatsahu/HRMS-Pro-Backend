import uuid


def generate_uuid() -> uuid.UUID:
    """
    Generate a new UUID4.
    """

    return uuid.uuid4()


def is_valid_uuid(value) -> bool:
    """
    Check whether a value is a valid UUID.
    """

    if isinstance(value, uuid.UUID):
        return True

    try:
        uuid.UUID(str(value))
        return True

    except (ValueError, TypeError, AttributeError):
        return False
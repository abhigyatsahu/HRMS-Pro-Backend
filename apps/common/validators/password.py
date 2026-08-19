from django.core.exceptions import ValidationError

from apps.common.constants import Auth


def validate_password_length(value):
    """
    Validate the minimum password length.
    """

    if not value:
        raise ValidationError(
            "Password is required."
        )

    if len(value) < Auth.PASSWORD_MIN_LENGTH:
        raise ValidationError(
            f"Password must contain at least "
            f"{Auth.PASSWORD_MIN_LENGTH} characters."
        )

    return value
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def validate_email_address(value):
    """
    Validate an email address using Django's
    built-in email validation.
    """

    if not value:
        raise ValidationError(
            "Email address is required."
        )

    value = str(value).strip().lower()

    validate_email(value)

    return value
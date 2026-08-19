from django.core.exceptions import ValidationError
import re
from apps.common.constants import Regex

def validate_phone_number(value):
    """
    Validate an Indian mobile phone number.
    """

    if not value:
        raise ValidationError(
            "Phone number is required."
        )

    value = str(value).strip()

    if not re.fullmatch(
        Regex.PHONE,
        value,
    ):
        raise ValidationError(
            "Enter a valid 10-digit mobile number."
        )

    return value
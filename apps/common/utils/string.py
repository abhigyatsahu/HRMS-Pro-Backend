import re
import secrets
import string


def normalize_spaces(value: str) -> str:
    """
    Remove unnecessary whitespace and normalize
    multiple spaces to a single space.
    """

    if value is None:
        return value

    return " ".join(
        str(value).strip().split()
    )


def generate_random_string(
    length: int = 32,
) -> str:
    """
    Generate a cryptographically secure random string.
    """

    characters = (
        string.ascii_letters
        + string.digits
    )

    return "".join(
        secrets.choice(characters)
        for _ in range(length)
    )


def generate_numeric_code(
    length: int = 6,
) -> str:
    """
    Generate a cryptographically secure numeric code.
    """

    if length <= 0:
        raise ValueError(
            "Length must be greater than zero."
        )

    return "".join(
        secrets.choice(string.digits)
        for _ in range(length)
    )


def slugify_text(value: str) -> str:
    """
    Create a simple URL-friendly slug.
    """

    value = normalize_spaces(value)

    value = value.lower()

    value = re.sub(
        r"[^a-z0-9\s-]",
        "",
        value,
    )

    value = re.sub(
        r"[\s_-]+",
        "-",
        value,
    )

    return value.strip("-")
from PIL import Image
from django.core.exceptions import ValidationError


def validate_image_dimensions(
    file,
    *,
    min_width,
    min_height,
    max_width,
    max_height,
):
    """
    Validate image dimensions.
    """

    if not file:
        raise ValidationError(
            "Image is required."
        )

    try:
        image = Image.open(file)

        width, height = image.size

    except Exception as exc:
        raise ValidationError(
            "Invalid image file."
        ) from exc

    if width < min_width or height < min_height:
        raise ValidationError(
            "Image dimensions are too small."
        )

    if width > max_width or height > max_height:
        raise ValidationError(
            "Image dimensions are too large."
        )

    return file

def validate_image(
    file,
    *,
    allowed_extensions,
    allowed_mime_types,
    max_size,
    min_width,
    min_height,
    max_width,
    max_height,
):
    """
    Validate image extension, MIME type,
    size and dimensions.
    """

    from .file import (
        validate_file_extension,
        validate_file_size,
        validate_mime_type,
    )

    validate_file_extension(
        file,
        allowed_extensions,
    )

    validate_file_size(
        file,
        max_size,
    )

    validate_mime_type(
        file,
        allowed_mime_types,
    )

    validate_image_dimensions(
        file,
        min_width=min_width,
        min_height=min_height,
        max_width=max_width,
        max_height=max_height,
    )

    return file
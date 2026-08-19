from pathlib import Path

from django.core.exceptions import ValidationError


def validate_file_extension(
    file,
    allowed_extensions,
):
    """
    Validate a file's extension.
    """

    if not file:
        raise ValidationError(
            "File is required."
        )

    extension = (
        Path(file.name)
        .suffix
        .lower()
    )

    if extension not in allowed_extensions:
        raise ValidationError(
            "File type is not allowed."
        )

    return file

def validate_file_size(
    file,
    max_size,
):
    """
    Validate uploaded file size.
    """

    if not file:
        raise ValidationError(
            "File is required."
        )

    if file.size > max_size:
        raise ValidationError(
            "File size exceeds the allowed limit."
        )

    return file

def validate_file(
    file,
    *,
    allowed_extensions,
    max_size,
):
    """
    Validate file extension and size.
    """

    validate_file_extension(
        file,
        allowed_extensions,
    )

    validate_file_size(
        file,
        max_size,
    )

    return file

'''
 validate_file(
#     uploaded_file,
#     allowed_extensions=FileExtension.DOCUMENT,
#     max_size=FileSize.MAX_DOCUMENT_SIZE,
# )
 
 Above sample method calling
'''

def validate_mime_type(
    file,
    allowed_mime_types,
):
    """
    Validate uploaded file MIME type.
    """

    if not file:
        raise ValidationError(
            "File is required."
        )

    content_type = getattr(
        file,
        "content_type",
        None,
    )

    if content_type not in allowed_mime_types:
        raise ValidationError(
            "Invalid file content type."
        )

    return file

'''
validate_mime_type(
    uploaded_file,
    MimeType.DOCUMENT,
)
'''
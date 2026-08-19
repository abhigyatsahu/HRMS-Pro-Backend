from pathlib import Path


def get_file_extension(
    filename: str,
) -> str:
    """
    Return a normalized file extension.
    """

    if not filename:
        return ""

    return Path(
        filename
    ).suffix.lower()


def get_filename_without_extension(
    filename: str,
) -> str:
    """
    Return the filename without its extension.
    """

    if not filename:
        return ""

    return Path(filename).stem


def get_file_size_in_mb(
    size_in_bytes: int,
) -> float:
    """
    Convert bytes to megabytes.
    """

    return round(
        size_in_bytes / (1024 * 1024),
        2,
    )
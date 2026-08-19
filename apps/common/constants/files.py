"""
File upload related constants.

This module centralizes all file-related configuration
used throughout the HRMS application.
"""


class FileSize:
    """
    File size limits (Bytes).
    """

    KB = 1024
    MB = 1024 * KB
    GB = 1024 * MB

    MAX_IMAGE_SIZE = 5 * MB
    MAX_DOCUMENT_SIZE = 10 * MB
    MAX_VIDEO_SIZE = 100 * MB
    MAX_EXCEL_SIZE = 20 * MB
    MAX_ZIP_SIZE = 100 * MB


class FileExtension:
    """
    Allowed file extensions.
    """

    IMAGE = (
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    )

    DOCUMENT = (
        ".pdf",
        ".doc",
        ".docx",
        ".txt",
    )

    EXCEL = (
        ".xls",
        ".xlsx",
        ".csv",
    )

    VIDEO = (
        ".mp4",
        ".mov",
        ".avi",
        ".mkv",
    )

    ARCHIVE = (
        ".zip",
        ".rar",
        ".7z",
    )


class MimeType:
    """
    Allowed MIME types.
    """

    IMAGE = (
        "image/jpeg",
        "image/png",
        "image/webp",
    )

    DOCUMENT = (
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
    )

    EXCEL = (
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "text/csv",
    )

    VIDEO = (
        "video/mp4",
        "video/quicktime",
        "video/x-msvideo",
        "video/x-matroska",
    )


class ImageDimension:
    """
    Image dimension limits.
    """

    MIN_WIDTH = 200
    MIN_HEIGHT = 200

    MAX_WIDTH = 5000
    MAX_HEIGHT = 5000

    COMPANY_LOGO_WIDTH = 512
    COMPANY_LOGO_HEIGHT = 512

    EMPLOYEE_PHOTO_WIDTH = 600
    EMPLOYEE_PHOTO_HEIGHT = 600


class UploadPath:
    """
    Upload directories.
    """

    COMPANY_LOGO = "company/logo/"

    EMPLOYEE_PHOTO = "employees/photos/"

    EMPLOYEE_DOCUMENT = "employees/documents/"

    PAYSLIP = "payroll/payslips/"

    ATTENDANCE_IMPORT = "attendance/imports/"

    REPORT_EXPORT = "reports/"

    TEMP = "temp/"


class ImageQuality:
    """
    Image processing constants.
    """

    JPEG_QUALITY = 90

    PNG_COMPRESS_LEVEL = 6

    WEBP_QUALITY = 90

class StorageDirectory:
    COMPANY = "company"
    EMPLOYEES = "employees"
    PAYROLL = "payroll"
    REPORTS = "reports"
    TEMP = "temp"
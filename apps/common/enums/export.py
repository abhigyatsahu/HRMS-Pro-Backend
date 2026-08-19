from .base import BaseEnum

class ExportFormat(BaseEnum):
    """
    Supported export formats.
    """

    CSV = "csv"

    XLSX = "xlsx"

    PDF = "pdf"
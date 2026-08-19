class CommonException(Exception):
    """
    Base exception for application-level exceptions.

    These exceptions are independent of HTTP/DRF.
    """

    default_message = "An application error occurred."
    default_code = "application_error"

    def __init__(
        self,
        message: str | None = None,
        *,
        code: str | None = None,
    ):
        self.message = (
            message
            or self.default_message
        )

        self.code = (
            code
            or self.default_code
        )

        super().__init__(self.message)
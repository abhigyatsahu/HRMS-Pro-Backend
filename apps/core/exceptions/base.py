from rest_framework import status


class HRMSException(Exception):
    """
    Base exception for HRMS.
    """

    status_code = status.HTTP_400_BAD_REQUEST

    default_message = "Something went wrong."

    default_code = "error"

    def __init__(
        self,
        message=None,
        code=None,
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
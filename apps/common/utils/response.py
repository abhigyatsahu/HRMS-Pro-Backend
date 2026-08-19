def success_payload(
    *,
    message: str,
    data=None,
):
    """
    Build a standard success payload.
    """

    return {
        "success": True,
        "message": message,
        "data": data,
    }


def error_payload(
    *,
    message: str,
    errors=None,
):
    """
    Build a standard error payload.
    """

    return {
        "success": False,
        "message": message,
        "errors": errors or {},
    }
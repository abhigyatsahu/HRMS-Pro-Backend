class Regex:
    PHONE = r"^[6-9]\d{9}$"

    PINCODE = r"^\d{6}$"

    PAN = r"^[A-Z]{5}[0-9]{4}[A-Z]$"

    GST = (
        r"^[0-9]{2}"
        r"[A-Z]{5}"
        r"[0-9]{4}"
        r"[A-Z]"
        r"[1-9A-Z]"
        r"Z"
        r"[0-9A-Z]$"
    )
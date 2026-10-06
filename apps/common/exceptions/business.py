from apps.core.exceptions.base import HRMSException


class BusinessRuleException(HRMSException):
    """
    Raised when a valid operation violates
    an application business rule.
    """

    status_code = 400
    code = "business_rule"
from .base import CommonException


class BusinessRuleException(CommonException):
    """
    Raised when a valid operation violates
    an application business rule.
    """

    default_message = "Business rule violated."

    default_code = "business_rule_violation"
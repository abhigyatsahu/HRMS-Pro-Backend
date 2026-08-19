from .base import BaseEnum


class NotificationChannel(BaseEnum):
    """
    Supported notification delivery channels.
    """

    EMAIL = "email"

    IN_APP = "in_app"

    PUSH = "push"

    SMS = "sms"
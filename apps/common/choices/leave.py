from django.db import models

class LeaveStatus(models.TextChoices):

    PENDING = "PENDING"

    APPROVED = "APPROVED"

    REJECTED = "REJECTED"

    CANCELED = "CANCELED"
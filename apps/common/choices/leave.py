from django.db import models

class LeaveStatus(models.Model):

    PENDING = "PENDING"

    APPROVED = "APPROVED"

    REJECTED = "REJECTED"

    CANCELED = "CANCELED"
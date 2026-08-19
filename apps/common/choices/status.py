from django.db import models

class StatusChoices(models.TextChoices):

    ACTIVE="ACTIVE"

    INACTIVE="INACTIVE"
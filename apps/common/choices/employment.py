from django.db import models

class EmploymentTypeChoices(models.TextChoices):

    FULL_TIME="FULL TIME"

    PART_TIME="PART TIME"

    CONTRACT="CONTRACT"

    INTERN="INTERN"

    CONSULTANT="CONSULTANT"
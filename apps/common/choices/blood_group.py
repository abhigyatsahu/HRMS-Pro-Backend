from django.db import models

class BloodGroupType(models.TextChoices):

    A_POSITIVE = "A+"

    A_NEGATIVE = "A-"

    B_NEGATIVE = "B-"

    B_POSITIVE = "B+"

    AB_POSITIVE = "AB+"

    AB_NEGATIVE = "AB-"

    O_NEGATIVE = "O-"

    O_POSITIVE = "O+"
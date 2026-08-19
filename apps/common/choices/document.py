from django.db import models

class DocumentType(models.TextChoices):

    RESUME = "RESUME"

    PAN = "PAN"

    AADHAR = "AADHAR"

    PASSPORT = "PASSPORT"

    OFFER_LETTER = "OFFER LETTER"

    EXPERIENCE_LETTER = "EXPERIENCE LETTER"

    PAYSLIP = "PAYSLIP"

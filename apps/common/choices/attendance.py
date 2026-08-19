from django.db import models

class AttendanceStatus(models.TextChoices):

    PRESENT = "PRESENT"

    ABSENT = "ABSENT"

    LATE = "LATE"

    HALF_DAY = "HALF DAY"

    HOLIDAY = "HOLIDAY"

    WEEKEND = "WEEKEND"

    LEAVE = "LEAVE"
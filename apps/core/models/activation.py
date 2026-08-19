from django.db import models


class ActivationModel(models.Model):

    is_active = models.BooleanField(
        default=True,
        db_index=True,
    )

    class Meta:
        abstract = True
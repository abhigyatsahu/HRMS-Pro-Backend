from django.db import models


class OrderingModel(models.Model):

    display_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
    )

    class Meta:
        abstract = True
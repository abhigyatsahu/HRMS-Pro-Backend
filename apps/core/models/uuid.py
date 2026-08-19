import uuid

from django.db import models


class UUIDModel(models.Model):
    """
    Abstract model providing UUID field.
    """

    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        db_index=True,
    )

    class Meta:
        abstract = True
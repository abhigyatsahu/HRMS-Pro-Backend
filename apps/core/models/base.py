from .activation import ActivationModel
from .timestamp import TimeStampedModel
from .uuid import UUIDModel


class BaseModel(
    UUIDModel,
    TimeStampedModel,
    ActivationModel,
):
    """
    Enterprise base model.
    """

    class Meta:
        abstract = True
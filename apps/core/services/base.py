import logging

from django.db import transaction


logger = logging.getLogger("hrms")


class BaseService:
    """
    Base service class for all business services.
    """

    logger = logger
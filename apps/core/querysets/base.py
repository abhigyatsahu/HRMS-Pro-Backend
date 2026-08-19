from django.db import models


class BaseQuerySet(models.QuerySet):

    def active(self):
        """
        Return only active records.
        """
        return self.filter(
            is_active=True
        )

    def inactive(self):
        """
        Return inactive records.
        """

        return self.filter(
            is_active=False
        )

    def newest(self):
        """
        Order newest first.
        """

        return self.order_by(
            "-created_at"
        )

    def oldest(self):
        """
        Order oldest first.
        """

        return self.order_by(
            "created_at"
        )

    def ordered(self):
        """
        Order by display order.
        """

        return self.order_by(
            "display_order",
            "created_at",
        )
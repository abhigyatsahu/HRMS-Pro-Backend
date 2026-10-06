from django.db import models

from apps.employees.querysets.employee import EmployeeQuerySet


class EmployeeManager(
    models.Manager.from_queryset(EmployeeQuerySet)
):
    def get_queryset(self):
        return super().get_queryset().not_deleted()
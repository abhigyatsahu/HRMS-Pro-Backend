from django.urls import path

from apps.employees.api.views import (
    EmployeeActivateView,
    EmployeeDeactivateView,
    EmployeeDetailView,
    EmployeeListCreateView,
    EmployeeRestoreView,
)


urlpatterns = [
    path(
        "",
        EmployeeListCreateView.as_view(),
        name="employee-list-create",
    ),
    path(
        "<uuid:uuid>/",
        EmployeeDetailView.as_view(),
        name="employee-detail",
    ),
    path(
        "<uuid:uuid>/restore/",
        EmployeeRestoreView.as_view(),
        name="employee-restore",
    ),
    path(
        "<uuid:uuid>/activate/",
        EmployeeActivateView.as_view(),
        name="employee-activate",
    ),
    path(
        "<uuid:uuid>/deactivate/",
        EmployeeDeactivateView.as_view(),
        name="employee-deactivate",
    ),
]
from django.urls import path

from apps.departments.api.views import (
    DepartmentActivateView,
    DepartmentDeactivateView,
    DepartmentDetailView,
    DepartmentListCreateView,
)


urlpatterns = [
    path(
        "",
        DepartmentListCreateView.as_view(),
        name="department-list-create",
    ),
    path(
        "<uuid:uuid>/",
        DepartmentDetailView.as_view(),
        name="department-detail",
    ),
    path(
        "<uuid:uuid>/activate/",
        DepartmentActivateView.as_view(),
        name="department-activate",
    ),
    path(
        "<uuid:uuid>/deactivate/",
        DepartmentDeactivateView.as_view(),
        name="department-deactivate",
    ),
]
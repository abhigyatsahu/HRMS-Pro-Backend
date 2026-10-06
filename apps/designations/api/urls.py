from django.urls import path

from .views import (
    DesignationListCreateView,
    DesignationDetailView,
    DesignationActivateView,
    DesignationDeactivateView,
    DesignationRestoreView,
    DesignationDeleteView,
)


urlpatterns = [
    path(
        "",
        DesignationListCreateView.as_view(),
        name="designation-list-create",
    ),

    path(
        "<uuid:uuid>/",
        DesignationDetailView.as_view(),
        name="designation-detail",
    ),

    path(
        "<uuid:uuid>/activate/",
        DesignationActivateView.as_view(),
        name="designation-activate",
    ),

    path(
        "<uuid:uuid>/deactivate/",
        DesignationDeactivateView.as_view(),
        name="designation-deactivate",
    ),

    path(
        "<uuid:uuid>/",
        DesignationDeleteView.as_view(),
        name="designation-delete",
    ),

    path(
        "<uuid:uuid>/restore/",
        DesignationRestoreView.as_view(),
        name="designation-restore",
    ),
]
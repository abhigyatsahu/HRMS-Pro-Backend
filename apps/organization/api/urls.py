from django.urls import path

from .views.organization_actions import (
    OrganizationActivateView,
    OrganizationDeactivateView,
)
from .views.organization_detail import (
    OrganizationDetailView,
)
from .views.organization_list import (
    OrganizationListCreateView,
)


urlpatterns = [
    path(
        "",
        OrganizationListCreateView.as_view(),
        name="organization-list-create",
    ),

    path(
        "<uuid:uuid>/",
        OrganizationDetailView.as_view(),
        name="organization-detail",
    ),

    path(
        "<uuid:uuid>/activate/",
        OrganizationActivateView.as_view(),
        name="organization-activate",
    ),

    path(
        "<uuid:uuid>/deactivate/",
        OrganizationDeactivateView.as_view(),
        name="organization-deactivate",
    ),
]
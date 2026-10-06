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

from .views.branch import (
    BranchListCreateView,
    BranchDetailView
)
from .views.branch_actions import (
    BranchActivateView,
    BranchDeactivateView
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
    path(
        "branches/",
        BranchListCreateView.as_view(),
        name="branch-list-create",
    ),

    path(
        "branches/<uuid:uuid>/",
        BranchDetailView.as_view(),
        name="branch-detail",
    ),

    path(
        "branches/<uuid:uuid>/activate/",
        BranchActivateView.as_view(),
        name="branch-activate",
    ),

    path(
        "branches/<uuid:uuid>/deactivate/",
        BranchDeactivateView.as_view(),
        name="branch-deactivate",
    ),
]
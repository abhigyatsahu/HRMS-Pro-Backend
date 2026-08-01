from django.urls import path

from .views.csrf import CSRFTokenView
from .views.login import LoginView
from .views.logout import LogoutView
from .views.me import CurrentUserView
from .views.refresh import RefreshTokenView


app_name = "accounts"


urlpatterns = [
    path(
        "csrf/",
        CSRFTokenView.as_view(),
        name="csrf",
    ),

    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),

    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    path(
        "refresh/",
        RefreshTokenView.as_view(),
        name="refresh",
    ),

    path(
        "me/",
        CurrentUserView.as_view(),
        name="me",
    ),
]
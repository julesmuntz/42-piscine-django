from django.urls import path
from .views import (
    AccountView,
    AuthLoginView,
    AuthLogoutView,
    AuthRegisterView,
    check_register,
)


urlpatterns = [
    path(
        "account/",
        AccountView.as_view(),
        name="account",
    ),
    path(
        "account/login/",
        AuthLoginView.as_view(),
        name="login",
    ),
    path(
        "account/register/",
        AuthRegisterView.as_view(),
        name="register",
    ),
    path(
        "account/logout/",
        AuthLogoutView.as_view(),
        name="logout",
    ),
    path(
        "ajax/check_register/",
        check_register,
        name="check_register",
    ),
]

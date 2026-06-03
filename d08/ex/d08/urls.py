"""
URL configuration for d08 project.

The `urlpatterns` list routes URLs to views. For more information please see:
        https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
        1. Add an import:  from my_app import views
        2. Add a URL to urlpatterns:  path('', views.account, name='account')
Class-based views
        1. Add an import:  from other_app.views import Account
        2. Add a URL to urlpatterns:  path('', Account.as_view(), name='account')
Including another URLconf
        1. Import the include() function: from django.urls import include, path
        2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(pattern_name="account", permanent=False)),
    path("", include("account.urls")),
    path(
        "account/login/",
        RedirectView.as_view(pattern_name="account", permanent=False),
    ),
    path(
        "account/register/",
        RedirectView.as_view(pattern_name="account", permanent=False),
    ),
    path(
        "account/logout/",
        RedirectView.as_view(pattern_name="account", permanent=False),
    ),
    path(
        "ajax/check_register/",
        RedirectView.as_view(pattern_name="account", permanent=False),
    ),
    path(
        "chatrooms/",
        RedirectView.as_view(pattern_name="account", permanent=False),
    ),
    path(
        "chatroom/<int:pk>/",
        RedirectView.as_view(pattern_name="account", permanent=False),
    ),
    path(
        "chatroom/<int:pk>/send_message/",
        RedirectView.as_view(pattern_name="account", permanent=False),
    ),
]

from django.urls import path
from .views import homepage

urlpatterns = [
    path(
        "",
        homepage,
        {
            "page_title": "Homepage",
        },
    ),
]

from django.urls import path
from .views import auth, homepage, logout


urlpatterns = [
    path(
        "",
        homepage,
        {
            "page_title": "Articles",
        },
    ),
    path(
        "login/",
        auth,
        {"page_title": "Login", "action": "Login"},
    ),
    path(
        "register/",
        auth,
        {"page_title": "Register", "action": "Register"},
    ),
    path("logout/", logout),
]

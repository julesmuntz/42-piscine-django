from django.urls import path
from .views import auth, logout


def get_urlpatterns(page_title):
    return [
        path(
            "",
            auth,
            {
                "page_title": page_title,
                "action": "Default"
            },
        ),
        path(
            "login/",
            auth,
            {
                "page_title": page_title + ": Login",
                "action": "Login"
            },
        ),
        path(
            "register/",
            auth,
            {
                "page_title": page_title + ": Register",
                "action": "Register"
            },
        ),
        path("logout/", logout),
    ]


page_title = "User Creation"

urlpatterns = get_urlpatterns(page_title)

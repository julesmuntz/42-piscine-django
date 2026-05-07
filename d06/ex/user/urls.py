from django.urls import path
from .views import status, auth, logout

urlpatterns = [
    # Ex00: Anonymous Sessions
    path(
        "status/",
        status,
        {
            "page_title": "Session Status",
        },
    ),

    # Ex01: User Creation
    path(
        "auth/",
        auth,
        {
            "page_title": "Authenticate",
            "action": "Default"
        },
    ),
    path(
        "login/",
        auth,
        {
            "page_title": "Login",
            "action": "Login"
        },
    ),
    path(
        "register/",
        auth,
        {
            "page_title": "Register",
            "action": "Register"
        },
    ),
    path("logout/", logout),
]

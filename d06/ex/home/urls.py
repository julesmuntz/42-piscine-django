from django.urls import path
from django.views.generic.base import RedirectView
from .views import auth, delete_tip, downvote, homepage, logout, status, upvote


urlpatterns = [
    # Ex00: Anonymous Sessions
    path(
        "",
        homepage,
        {
            "page_title": "Life Pro Tips",
        },
    ),
    path(
        "status/",
        status,
        {
            "page_title": "Session Status",
        },
    ),
    # Ex01: User Creation (legacy /auth/ → login)
    path(
        "auth/",
        RedirectView.as_view(url="/login/", query_string=True),
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
    path("tips/<int:tip_id>/delete/", delete_tip),
    path("tips/<int:tip_id>/upvote/", upvote),
    path("tips/<int:tip_id>/downvote/", downvote),
]

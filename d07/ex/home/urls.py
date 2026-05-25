from django.urls import path

from .views import (
    HomeView,
    AuthLoginView,
    AuthRegisterView,
    AuthLogoutView,
    ArticleListView,
    ArticleView,
    PublicationListView,
    PublicationView,
    FavoriteArticlesView,
    AddFavoriteArticleView,
)


urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    path(
        "login/",
        AuthLoginView.as_view(),
        name="login",
    ),
    path(
        "register/",
        AuthRegisterView.as_view(),
        name="register",
    ),
    path("logout/", AuthLogoutView.as_view(), name="logout"),
    path(
        "articles/",
        ArticleListView.as_view(),
        name="articles",
    ),
    path(
        "article/<int:pk>/",
        ArticleView.as_view(),
        name="article",
    ),
    path(
        "publications/",
        PublicationListView.as_view(),
        name="publications",
    ),
    path(
        "publication/<int:pk>/",
        PublicationView.as_view(),
        name="publication",
    ),

    path(
        "favorites/",
        FavoriteArticlesView.as_view(),
        name="favorites",
    ),
    path(
        "favorite/<int:pk>/",
        AddFavoriteArticleView.as_view(),
        name="favorite",
    ),
]

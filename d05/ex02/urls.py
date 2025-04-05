from django.urls import path
from ex00.views import init
from . import views

urlpatterns = [
	path("init/", init, {"table_name": "ex02_movies"}),
	path("populate/", views.populate, {"table_name": "ex02_movies", "use_sql": True}),
	path("display/", views.display, {"table_name": "ex02_movies", "use_sql": True}),
]

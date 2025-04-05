from django.urls import path
from . import views

urlpatterns = [
	path("init/", views.init, {"table_name": "ex00_movies"}),
]

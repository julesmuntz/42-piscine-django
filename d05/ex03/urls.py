from django.urls import path
from ex02.views import populate, display

urlpatterns = [
	path("populate/", populate, {"table_name": "ex03_movies", "use_sql": False}),
	path("display/", display, {"table_name": "ex03_movies", "use_sql": False}),
]

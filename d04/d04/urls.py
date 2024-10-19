from django.urls import include, path

urlpatterns = [
	path("ex00/", include("ex00.urls")),
	path("ex01/", include("ex01.urls")),
]

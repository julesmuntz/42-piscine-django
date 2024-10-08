from django.urls import path
from . import views

urlpatterns = [
	path("ex00/", views.ex00, name="ex00"),
]

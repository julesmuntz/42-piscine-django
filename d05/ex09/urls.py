from django.urls import path
from .views import display

page_title = "ORM - Foreign Key"

urlpatterns = [
	path(
		"display/",
		display,
		{
			"page_title": page_title,
		},
	),
]

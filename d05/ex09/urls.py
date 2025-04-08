from django.urls import path
from .views import display

page_title = "ORM - Foreign Key"
table_name = "ex09_planets and ex09_people"

urlpatterns = [
	path(
		"display/",
		display,
		{
			"table_name": table_name,
			"page_title": page_title,
		},
	),
]

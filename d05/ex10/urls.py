from django.urls import path
from .views import search

page_title = "ORM - Many to Many"

urlpatterns = [
	path(
		"",
		search,
		{
			"page_title": page_title,
		},
	),
]

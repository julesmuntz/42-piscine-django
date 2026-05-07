from django.urls import path
from .views import tips

urlpatterns = [
	path(
		"tips/",
		tips,
		{
			"page_title": "Tips",
		},
	),
]

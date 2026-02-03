from django.urls import path
from .views import hello


def get_urlpatterns(page_title):
	return [
		path(
			"hello/",
			hello,
			{
				"page_title": page_title,
			},
		),
	]


page_title = "Anonymous Sessions"

urlpatterns = get_urlpatterns(page_title)

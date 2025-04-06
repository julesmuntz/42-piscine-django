from django.urls import path
from ex03.urls import get_base_patterns
from .views import remove


def get_urlpatterns(table_name, page_title):
	base_patterns = get_base_patterns(table_name, page_title)
	return base_patterns + [
		path(
			"remove/",
			remove,
			{
				"table_name": table_name,
				"page_title": page_title,
			},
		),
	]


page_title = "SQL - Data Deleting"
table_name = "ex04_movies"

urlpatterns = get_urlpatterns(table_name, page_title)

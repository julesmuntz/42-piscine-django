from django.urls import path
from ex00.urls import get_urlpatterns as get_base_patterns
from .views import populate, display


def get_urlpatterns(table_name, page_title):
	patterns = []
	if page_title[:3] == "SQL":
		patterns.extend(get_base_patterns(table_name, page_title))

	patterns.extend(
		[
			path(
				"populate/",
				populate,
				{
					"table_name": table_name,
					"page_title": page_title,
				},
			),
			path(
				"display/",
				display,
				{
					"table_name": table_name,
					"page_title": page_title,
				},
			),
		]
	)
	return patterns


page_title = "SQL - Data Insertion"
table_name = "ex02_movies"

urlpatterns = get_urlpatterns(table_name, page_title)

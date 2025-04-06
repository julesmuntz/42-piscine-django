from django.urls import path
from ex03.urls import get_base_patterns
from .views import remove


def get_urlpatterns(table_name, use_sql, page_title):
	base_patterns = get_base_patterns(table_name, use_sql, page_title)
	return base_patterns + [
		path(
			"remove/",
			remove,
			{
				"table_name": table_name,
				"use_sql": use_sql,
				"page_title": page_title,
			},
		),
	]


page_title = "SQL - Data Deleting"
table_name = "ex04_movies"
use_sql = True

urlpatterns = get_urlpatterns(table_name, use_sql, page_title)

from django.urls import path
from ex00.urls import get_urlpatterns as get_base_patterns
from .views import populate, display


def get_urlpatterns(table_name, use_sql, page_title):
	base_patterns = get_base_patterns(table_name, use_sql, page_title)
	return base_patterns + [
		path(
			"populate/",
			populate,
			{
				"table_name": table_name,
				"use_sql": use_sql,
				"page_title": page_title,
			},
		),
		path(
			"display/",
			display,
			{
				"table_name": table_name,
				"use_sql": use_sql,
				"page_title": page_title,
			},
		),
	]


page_title = "SQL - Data Insertion"
table_name = "ex02_movies"
use_sql = True

urlpatterns = get_urlpatterns(table_name, use_sql, page_title)

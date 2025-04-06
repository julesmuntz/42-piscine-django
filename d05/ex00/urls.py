from django.urls import path
from .views import init


def get_urlpatterns(table_name, use_sql, page_title):
	return [
		path(
			"init/",
			init,
			{
				"table_name": table_name,
				"use_sql": use_sql,
				"page_title": page_title,
			},
		),
	]


page_title = "SQL - Building a Table"
table_name = "ex00_movies"
use_sql = True

urlpatterns = get_urlpatterns(table_name, use_sql, page_title)

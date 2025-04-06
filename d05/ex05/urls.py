from ex04.urls import get_urlpatterns as get_base_patterns

page_title = "ORM - Deleting Data"
table_name = "ex05_movies"

urlpatterns = get_base_patterns(table_name, page_title)

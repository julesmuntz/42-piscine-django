from ex06.urls import get_urlpatterns as get_base_patterns

page_title = "ORM - Updating a data"
table_name = "ex07_movies"

urlpatterns = get_base_patterns(table_name, page_title)

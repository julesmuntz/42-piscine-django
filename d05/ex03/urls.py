from ex02.urls import get_urlpatterns as get_base_patterns

page_title = "ORM - Data Insertion"
table_name = "ex03_movies"

urlpatterns = get_base_patterns(table_name, page_title)

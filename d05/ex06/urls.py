from django.urls import path
from ex03.urls import get_base_patterns
from .views import update
from ex00.views import init

init.sql_command = """
	CREATE TABLE IF NOT EXISTS ex06_movies (
		title VARCHAR(64) NOT NULL,
		episode_nb INTEGER PRIMARY KEY,
		opening_crawl TEXT,
		director VARCHAR(32) NOT NULL,
		producer VARCHAR(128) NOT NULL,
		release_date DATE NOT NULL,
		created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
		updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	);

	DROP TRIGGER IF EXISTS update_films_changetimestamp ON ex06_movies;
	DROP FUNCTION IF EXISTS update_changetimestamp_column();

	CREATE OR REPLACE FUNCTION update_changetimestamp_column()
	RETURNS TRIGGER AS $$
	BEGIN
		NEW.updated = now();
		NEW.created = OLD.created;
		RETURN NEW;
	END;
	$$ language 'plpgsql';

	CREATE TRIGGER update_films_changetimestamp
	BEFORE UPDATE ON ex06_movies
	FOR EACH ROW EXECUTE PROCEDURE update_changetimestamp_column();
"""


def get_urlpatterns(table_name, page_title):
	base_patterns = get_base_patterns(table_name, page_title)
	return base_patterns + [
		path(
			"update/",
			update,
			{
				"table_name": table_name,
				"page_title": page_title,
			},
		),
	]


page_title = "SQL - Updating a data"
table_name = "ex06_movies"

urlpatterns = get_urlpatterns(table_name, page_title)

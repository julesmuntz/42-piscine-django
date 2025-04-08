from django.urls import path
from ex00.urls import get_urlpatterns as get_base_patterns
from .views import populate, display
from ex00.views import init

init.ex08_sql = """
	CREATE TABLE IF NOT EXISTS ex08_planets (
		id SERIAL PRIMARY KEY,
		name VARCHAR(64) UNIQUE NOT NULL,
		climate VARCHAR(255),
		diameter INTEGER,
		orbital_period INTEGER,
		population BIGINT,
		rotation_period INTEGER,
		surface_water REAL,
		terrain VARCHAR(128)
	);
	CREATE TABLE IF NOT EXISTS ex08_people (
		id SERIAL PRIMARY KEY,
		name VARCHAR(64) UNIQUE NOT NULL,
		birth_year VARCHAR(32),
		gender VARCHAR(32),
		eye_color VARCHAR(32),
		hair_color VARCHAR(32),
		height INTEGER,
		mass REAL,
		homeworld VARCHAR(64) REFERENCES ex08_planets(name)
	);
"""

init.tables = {"ex08_planets and ex08_people": ["ex08_planets", "ex08_people"]}


def get_urlpatterns(page_title):
	patterns = []
	patterns.extend(get_base_patterns("ex08_planets and ex08_people", page_title))

	patterns.extend(
		[
			path(
				"populate/",
				populate,
				{
					"page_title": page_title,
				},
			),
			path(
				"display/",
				display,
				{
					"page_title": page_title,
				},
			),
		]
	)
	return patterns


page_title = "SQL - Foreign Key"

urlpatterns = get_urlpatterns(page_title)

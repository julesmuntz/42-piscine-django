from ex03.urls import get_base_patterns
from ex00.views import init, get_db_connection
from ex02.views import populate
import os
import csv

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


def ex08_data():
	planets_csv_path = os.path.join(
		os.path.dirname(__file__), "..", "d05", "static", "data", "planets.csv"
	)
	planets_data = []
	with open(planets_csv_path, "r") as file:
		reader = csv.reader(file, delimiter="\t")
		for row in reader:
			planets_data.append(row)

	people_csv_path = os.path.join(
		os.path.dirname(__file__), "..", "d05", "static", "data", "people.csv"
	)
	people_data = []
	with open(people_csv_path, "r") as file:
		reader = csv.reader(file, delimiter="\t")
		for row in reader:
			people_data.append(row)

	return {"planets": planets_data, "people": people_data}


def ex08_sql_insert(data):
	messages = []
	conn = get_db_connection()
	try:
		planets_data = data["planets"]
		planets_values = []
		for row in planets_data:
			planets_values.append(
				(
					row[0],
					row[1] if row[1] != "NULL" else None,
					int(row[2]) if row[2] != "NULL" else None,
					int(row[3]) if row[3] != "NULL" else None,
					int(row[4]) if row[4] != "NULL" else None,
					int(row[5]) if row[5] != "NULL" else None,
					float(row[6]) if row[6] != "NULL" else None,
					row[7] if row[7] != "NULL" else None,
				)
			)
		with conn.cursor() as cur:
			cur.execute("SELECT name FROM ex08_planets")
			existing_planets = {row[0] for row in cur.fetchall()}
			new_planets = []
			for planet in planets_values:
				if planet[0] in existing_planets:
					messages.append(f"ERROR: Planet '{planet[0]}' already exists")
				else:
					new_planets.append(planet)
					messages.append("OK")
			if new_planets:
				args_str = ",".join(
					cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s)", x).decode("utf-8")
					for x in new_planets
				)
				cur.execute(
					"""
					INSERT INTO ex08_planets
					(name, climate, diameter, orbital_period, population, rotation_period,
					surface_water, terrain)
					VALUES """
					+ args_str
				)
			conn.commit()

		people_data = data["people"]
		people_values = []
		for row in people_data:
			people_values.append(
				(
					row[0],
					row[1] if row[1] != "NULL" else None,
					row[2] if row[2] != "NULL" else None,
					row[3] if row[3] != "NULL" else None,
					row[4] if row[4] != "NULL" else None,
					int(row[5]) if row[5] != "NULL" else None,
					float(row[6]) if row[6] != "NULL" else None,
					row[7] if row[7] != "NULL" else None,
				)
			)
		with conn.cursor() as cur:
			cur.execute("SELECT name FROM ex08_people")
			existing_people = {row[0] for row in cur.fetchall()}
			new_people = []
			for person in people_values:
				if person[0] in existing_people:
					messages.append(f"ERROR: Person '{person[0]}' already exists")
				else:
					new_people.append(person)
					messages.append("OK")
			if new_people:
				args_str = ",".join(
					cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s)", x).decode("utf-8")
					for x in new_people
				)
				cur.execute(
					"""
					INSERT INTO ex08_people
					(name, birth_year, gender, eye_color, hair_color, height, mass, homeworld)
					VALUES """
					+ args_str
				)
			conn.commit()

	except Exception as e:
		conn.rollback()
		error_parts = str(e).split("DETAIL:")
		if len(error_parts) > 1:
			messages.extend([part.strip() for part in error_parts])
		else:
			messages.append(str(e))
	finally:
		conn.close()

	return messages


populate.ex08_data = ex08_data
populate.ex08_sql_insert = ex08_sql_insert

init.tables = {"ex08": ["ex08_planets", "ex08_people"]}

page_title = "SQL - Foreign Key"
table_name = "ex08"

urlpatterns = get_base_patterns(table_name, page_title)

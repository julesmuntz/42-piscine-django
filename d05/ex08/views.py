from django.shortcuts import render
from ex00.views import get_db_connection
import os
import csv
import io


def populate(request, table_name, page_title):
	messages = []

	if request.method == "POST":
		planets_csv_path = os.path.join(
			os.path.dirname(__file__), "..", "d05", "static", "data", "planets.csv"
		)
		people_csv_path = os.path.join(
			os.path.dirname(__file__), "..", "d05", "static", "data", "people.csv"
		)

		conn = get_db_connection()
		try:
			with conn.cursor() as cur:
				cur.execute("SELECT name FROM ex08_planets")
				existing_planets = {row[0] for row in cur.fetchall()}

			planets_data = io.StringIO()

			with open(planets_csv_path, "r") as file:
				reader = csv.reader(file, delimiter="\t")
				for row in reader:
					if row[0] not in existing_planets:
						planets_data.write("\t".join(row) + "\n")
						messages.append("OK")
					else:
						messages.append(f"ERROR: Planet '{row[0]}' already exists")

			if planets_data.getvalue():
				planets_data.seek(0)
				with conn.cursor() as cur:
					cur.copy_from(
						planets_data,
						"ex08_planets",
						columns=(
							"name",
							"climate",
							"diameter",
							"orbital_period",
							"population",
							"rotation_period",
							"surface_water",
							"terrain",
						),
						null="NULL",
					)
				conn.commit()

			with conn.cursor() as cur:
				cur.execute("SELECT name FROM ex08_people")
				existing_people = {row[0] for row in cur.fetchall()}

			people_data = io.StringIO()

			with open(people_csv_path, "r") as file:
				reader = csv.reader(file, delimiter="\t")
				for row in reader:
					if row[0] not in existing_people:
						people_data.write("\t".join(row) + "\n")
						messages.append("OK")
					else:
						messages.append(f"ERROR: Person '{row[0]}' already exists")

			if people_data.getvalue():
				people_data.seek(0)
				with conn.cursor() as cur:
					cur.copy_from(
						people_data,
						"ex08_people",
						columns=(
							"name",
							"birth_year",
							"gender",
							"eye_color",
							"hair_color",
							"height",
							"mass",
							"homeworld",
						),
						null="NULL",
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

	return render(
		request,
		"d05/templates/form.html",
		{
			"title": page_title,
			"messages": messages,
			"label": f"Insert data into {table_name}",
		},
	)


def display(request, table_name, page_title):
	messages = []
	rows = []

	try:
		conn = get_db_connection()
		with conn.cursor() as cur:
			cur.execute(
				"""
				SELECT p.name, p.homeworld, pl.climate
				FROM ex08_people p
				JOIN ex08_planets pl ON p.homeworld = pl.name
				WHERE pl.climate LIKE '%windy%' OR pl.climate LIKE '%moderately windy%'
				ORDER BY p.name ASC
			"""
			)

			query_results = cur.fetchall()

			if query_results:
				rows = query_results
			else:
				messages = ["No data available"]

	except Exception:
		messages = ["No data available"]

	finally:
		if "conn" in locals():
			conn.close()

	return render(
		request,
		"d05/templates/display2.html",
		{
			"title": page_title,
			"messages": messages,
			"rows": rows,
			"table_name": table_name,
		},
	)

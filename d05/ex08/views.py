from django.shortcuts import render
from ex00.views import get_db_connection
import os
import csv
import io


def populate(request, page_title):
	messages = []

	if request.method == "POST":
		data_config = [
			{
				"name": "planets",
				"csv_path": os.path.join(os.path.dirname(__file__), "..", "d05", "static", "data", "planets.csv"),
				"table_name": "ex08_planets",
				"columns": (
					"name",
					"climate",
					"diameter",
					"orbital_period",
					"population",
					"rotation_period",
					"surface_water",
					"terrain",
				),
			},
			{
				"name": "people",
				"csv_path": os.path.join(os.path.dirname(__file__), "..", "d05", "static", "data", "people.csv"),
				"table_name": "ex08_people",
				"columns": (
					"name",
					"birth_year",
					"gender",
					"eye_color",
					"hair_color",
					"height",
					"mass",
					"homeworld",
				),
			},
		]

		conn = get_db_connection()

		for config in data_config:
			try:
				with conn.cursor() as cur:
					cur.execute(f"SELECT name FROM {config['table_name']}")
					existing_entries = {row[0] for row in cur.fetchall()}

				data_buffer = io.StringIO()

				with open(config["csv_path"], "r") as file:
					reader = csv.reader(file, delimiter="\t")
					for row in reader:
						if row[0] not in existing_entries:
							data_buffer.write("\t".join(row) + "\n")
							messages.append("OK")
						else:
							messages.append(f"ERROR: {config['name'].capitalize()[:-1]} '{row[0]}' already exists")

				if data_buffer.getvalue():
					data_buffer.seek(0)
					with conn.cursor() as cur:
						cur.copy_from(
							data_buffer,
							config["table_name"],
							columns=config["columns"],
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

		conn.close()

	return render(
		request,
		"d05/templates/form.html",
		{
			"title": page_title,
			"messages": messages,
			"label": "Insert data into ex08_planets and ex08_people",
		},
	)


def display(request, page_title):
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
		conn.close()

	except Exception:
		messages = ["No data available"]

	return render(
		request,
		"d05/templates/display2.html",
		{
			"title": page_title,
			"messages": messages,
			"rows": rows,
			"table_name": "ex08_planets and ex08_people",
		},
	)

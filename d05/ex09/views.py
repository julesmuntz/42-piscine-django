from django.shortcuts import render
from django.db.models import Q
from ex09.models import People


def display(request, table_name, page_title):
	messages = []
	rows = []

	try:
		people_with_windy_planets = (
			People.objects.filter(
				Q(homeworld__climate__contains="windy")
				| Q(homeworld__climate__contains="moderately windy")
			)
			.select_related("homeworld")
			.order_by("name")
		)

		if people_with_windy_planets:
			for person in people_with_windy_planets:
				rows.append(
					(
						person.name,
						person.homeworld.name,
						person.homeworld.climate,
					)
				)
		else:
			messages = [
				"No data available, please use the following command line before use:",
				"python manage.py loaddata d05/static/data/ex09_initial_data.json",
			]

	except Exception:
		messages = [
			"No data available, please use the following command line before use:",
			"python manage.py loaddata d05/static/data/ex09_initial_data.json",
		]

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

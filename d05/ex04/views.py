from django.shortcuts import render
from ex00.views import get_db_connection
from importlib import import_module


def remove(request, table_name, use_sql, page_title):
	messages = []
	titles = []
	try:
		if request.method == "POST":
			title_to_remove = request.POST.get("title")
			if title_to_remove:
				if use_sql:
					with get_db_connection() as conn:
						cur = conn.cursor()
						cur.execute(f"DELETE FROM {table_name} WHERE title = %s;", [title_to_remove])
						conn.commit()
						if cur.rowcount <= 0:
							messages.append("No data available")
						else:
							messages.append("OK")
				else:
					module = import_module(f"ex{int(table_name[2:4]):02d}.models")
					Movies = module.Movies
					deleted = Movies.objects.filter(title=title_to_remove).delete()
					if deleted[0] > 0:
						messages.append("OK")
					else:
						messages.append("No data available")
		if use_sql:
			with get_db_connection() as conn:
				cur = conn.cursor()
				cur.execute(f"SELECT title FROM {table_name} ORDER BY episode_nb;")
				titles = [row[0] for row in cur.fetchall()]
		else:
			titles = [movie.title for movie in Movies.objects.all().order_by("episode_nb")]
		if not titles:
			messages = ["No data available"]

	except Exception as e:
		error_parts = str(e).split("DETAIL:")
		if len(error_parts) > 1:
			messages = [part.strip() for part in error_parts]
		else:
			messages = [str(e)]

	return render(
		request,
		"d05/templates/dropdown.html",
		{
			"title": page_title,
			"label": "remove",
			"messages": messages,
			"titles": titles,
		},
	)

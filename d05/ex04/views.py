from django.shortcuts import render
from ex00.views import get_db_connection
from importlib import import_module


def remove(request, table_name, page_title):
	messages = []
	titles = []
	try:
		if request.method == "POST":
			title_to_remove = request.POST.get("title")
			if title_to_remove:
				if page_title[:3] == "SQL":
					with get_db_connection() as conn:
						cur = conn.cursor()
						cur.execute(
							f"DELETE FROM {table_name} WHERE title = %s;",
							[title_to_remove],
						)
						conn.commit()
						if cur.rowcount <= 0:
							messages = ["No data available"]
						else:
							messages = ["OK"]
				elif page_title[:3] == "ORM":
					module = import_module(f"ex{int(table_name[2:4]):02d}.models")
					Movies = module.Movies
					deleted = Movies.objects.filter(title=title_to_remove).delete()
					if deleted[0] > 0:
						messages = ["OK"]
					else:
						messages = ["No data available"]
		if page_title[:3] == "SQL":
			with get_db_connection() as conn:
				cur = conn.cursor()
				cur.execute(f"SELECT title FROM {table_name} ORDER BY episode_nb;")
				titles = [row[0] for row in cur.fetchall()]
		elif page_title[:3] == "ORM":
			module = import_module(f"ex{int(table_name[2:4]):02d}.models")
			Movies = module.Movies
			titles = [movie.title for movie in Movies.objects.all().order_by("episode_nb")]
		if not titles:
			messages = ["No data available"]

	except Exception:
		messages = ["No data available"]

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

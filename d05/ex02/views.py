from django.shortcuts import render
from ex00.views import get_db_connection
from importlib import import_module
from datetime import datetime
import json
import os


def populate(request, table_name, page_title):
	messages = []

	if request.method == "POST":
		json_path = os.path.join(
			os.path.dirname(__file__), "static", "data", "opening_crawl.json"
		)
		try:
			with open(json_path, "r") as file:
				opening_crawls = json.load(file)
		except Exception as e:
			messages.append(f"Error loading opening crawls: {str(e)}")
			opening_crawls = {}
		data = [
			(
				1,
				"The Phantom Menace",
				"George Lucas",
				"Rick McCallum",
				"1999-05-19",
				opening_crawls.get("The Phantom Menace", ""),
			),
			(
				2,
				"Attack of the Clones",
				"George Lucas",
				"Rick McCallum",
				"2002-05-16",
				opening_crawls.get("Attack of the Clones", ""),
			),
			(
				3,
				"Revenge of the Sith",
				"George Lucas",
				"Rick McCallum",
				"2005-05-19",
				opening_crawls.get("Revenge of the Sith", ""),
			),
			(
				4,
				"A New Hope",
				"George Lucas",
				"Gary Kurtz, Rick McCallum",
				"1977-05-25",
				opening_crawls.get("A New Hope", ""),
			),
			(
				5,
				"The Empire Strikes Back",
				"Irvin Kershner",
				"Gary Kurtz, Rick McCallum",
				"1980-05-17",
				opening_crawls.get("The Empire Strikes Back", ""),
			),
			(
				6,
				"Return of the Jedi",
				"Richard Marquand",
				"Howard G. Kazanjian, George Lucas, Rick McCallum",
				"1983-05-25",
				opening_crawls.get("Return of the Jedi", ""),
			),
			(
				7,
				"The Force Awakens",
				"J.J. Abrams",
				"Kathleen Kennedy, J.J. Abrams, Bryan Burk",
				"2015-12-11",
				opening_crawls.get("The Force Awakens", ""),
			),
		]

		if page_title[:3] == "SQL":
			try:
				conn = get_db_connection()
				with conn.cursor() as cur:
					for movie in data:
						try:
							cur.execute(
								f"""
								INSERT INTO {table_name}
								(episode_nb, title, director, producer, release_date, opening_crawl)
								VALUES
								(%s, %s, %s, %s, %s, %s)
								""",
								(
									movie[0],
									movie[1],
									movie[2],
									movie[3],
									datetime.strptime(movie[4], "%Y-%m-%d"),
									movie[5],
								),
							)
							conn.commit()
							messages.append("OK")
						except Exception as e:
							error_parts = str(e).split("DETAIL:")
							if len(error_parts) > 1:
								messages.extend([part.strip() for part in error_parts])
							else:
								messages.append(str(e))
							conn.rollback()
			except Exception as e:
				messages.append(str(e))
			finally:
				conn.close()
		elif page_title[:3] == "ORM":
			module = import_module(f"ex{int(table_name[2:4]):02d}.models")
			Movies = module.Movies
			for movie in data:
				try:
					Movies.objects.create(
						episode_nb=movie[0],
						title=movie[1],
						director=movie[2],
						producer=movie[3],
						release_date=datetime.strptime(movie[4], "%Y-%m-%d"),
						opening_crawl=movie[5],
					)
					messages.append("OK")
				except Exception as e:
					messages.append(str(e))

	return render(
		request,
		"d05/templates/form.html",
		{
			"title": page_title,
			"messages": messages,
			"label": f"Insert data into {table_name}",
		},
	)


def to_roman(num):
	val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
	syms = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
	roman_num = ""
	i = 0
	while num > 0:
		for _ in range(num // val[i]):
			roman_num += syms[i]
			num -= val[i]
		i += 1
	return roman_num


def display(request, table_name, page_title):
	messages = []
	roman_rows = []
	try:
		if page_title[:3] == "SQL":
			with get_db_connection() as conn:
				cur = conn.cursor()
				if table_name == "ex06_movies":
					cur.execute(
						f"SELECT episode_nb, title, director, producer, release_date, opening_crawl, created, updated "
						f"FROM {table_name} ORDER BY episode_nb;"
					)
				else:
					cur.execute(
						f"SELECT episode_nb, title, director, producer, release_date, opening_crawl "
						f"FROM {table_name} ORDER BY episode_nb;"
					)
				rows = cur.fetchall()
				if rows:
					for row in rows:
						if table_name == "ex06_movies":
							roman_rows.append(
								(
									to_roman(row[0]),
									row[1],
									row[2],
									row[3],
									row[4],
									row[5],
									row[6],
									row[7],
								)
							)
						else:
							roman_rows.append(
								(
									to_roman(row[0]),
									row[1],
									row[2],
									row[3],
									row[4],
									row[5],
								)
							)
				else:
					messages = ["No data available"]
		elif page_title[:3] == "ORM":
			module = import_module(f"ex{int(table_name[2:4]):02d}.models")
			Movies = module.Movies
			movies = Movies.objects.all().order_by("episode_nb")
			if movies:
				for movie in movies:
					if table_name == "ex07_movies":
						roman_rows.append(
							(
								to_roman(movie.episode_nb),
								movie.title,
								movie.director,
								movie.producer,
								movie.release_date,
								movie.opening_crawl,
								movie.created,
								movie.updated,
							)
						)
					else:
						roman_rows.append(
							(
								to_roman(movie.episode_nb),
								movie.title,
								movie.director,
								movie.producer,
								movie.release_date,
								movie.opening_crawl,
							)
						)
			else:
				messages = ["No data available"]
	except Exception:
		messages = ["No data available"]

	return render(
		request,
		"d05/templates/display.html",
		{
			"title": page_title,
			"messages": messages,
			"rows": roman_rows,
			"table_name": table_name,
		},
	)

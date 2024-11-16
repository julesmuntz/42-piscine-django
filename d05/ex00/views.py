from django.shortcuts import render
import psycopg2
from decouple import config


def create_movies_table(conn):
	try:
		commands = (
			"""
			CREATE TABLE ex00_movies (
				title VARCHAR(64) NOT NULL,
				episode_nb INTEGER PRIMARY KEY,
				opening_crawl TEXT NOT NULL,
				director VARCHAR(32) NOT NULL,
				producer VARCHAR(128) NOT NULL,
				release_date DATE NOT NULL
			)
			""",
		)
		with conn.cursor() as cur:
			for command in commands:
				cur.execute(command)
		return "OK"
	except (psycopg2.DatabaseError, Exception) as error:
		return error


def init(request):
	message = "OK"
	with psycopg2.connect(
		dbname=config("DB_NAME"),
		user=config("DB_USER"),
		password=config("DB_PASSWORD"),
		host=config("DB_HOST"),
		port=config("DB_PORT"),
	) as conn:
		cur = conn.cursor()
		cur.execute(
			"SELECT EXISTS(SELECT relname FROM pg_class WHERE relname='ex00_movies')"
		)
		exist = cur.fetchone()[0]
		cur.close()
		if not exist:
			message = "relation \"ex00_movies\" does not exist"
		if request.method == "POST":
			message = create_movies_table(conn)

	return render(
		request,
		"d05/templates/init.html",
		{
			"title": "SQL - Building a Table",
			"message": message,
		},
	)

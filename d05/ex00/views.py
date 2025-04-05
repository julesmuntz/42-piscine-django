from django.shortcuts import render
import psycopg2
from decouple import config


def get_db_connection():
	"""Create and return a database connection"""
	return psycopg2.connect(
		dbname=config("DB_NAME"),
		user=config("DB_USER"),
		password=config("DB_PASSWORD"),
		host=config("DB_HOST"),
		port=config("DB_PORT"),
	)


def create_movies_table(conn, table_name):
	try:
		commands = (
			f"""
			CREATE TABLE {table_name} (
				title VARCHAR(64) NOT NULL,
				episode_nb INTEGER PRIMARY KEY,
				opening_crawl TEXT,
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


def init(request, table_name):
	message = "OK"
	try:
		with get_db_connection() as conn:
			cur = conn.cursor()
			cur.execute(f"SELECT EXISTS(SELECT relname FROM pg_class WHERE relname='{table_name}')")
			exist = cur.fetchone()[0]
			if not exist:
				message = f'relation "{table_name}" does not exist'
			if request.method == "POST":
				message = create_movies_table(conn, table_name)
	except psycopg2.Error as e:
		message = str(e)

	return render(
		request,
		"d05/templates/form.html",
		{
			"title": "SQL - Building a Table",
			"label": f"init {table_name} table",
			"message": message,
		},
	)

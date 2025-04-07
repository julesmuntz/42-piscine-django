from django.shortcuts import render
import psycopg2
from decouple import config


def get_db_connection():
	return psycopg2.connect(
		dbname=config("DB_NAME"),
		user=config("DB_USER"),
		password=config("DB_PASSWORD"),
		host=config("DB_HOST"),
		port=config("DB_PORT"),
	)


def init(request, table_name, page_title):
	messages = []
	try:
		with get_db_connection() as conn:
			cur = conn.cursor()
			cur.execute(
				f"SELECT EXISTS(SELECT relname FROM pg_class WHERE relname='{table_name}')"
			)
			exist = cur.fetchone()[0]
			if request.method == "POST":
				if exist:
					messages = [f'Table "{table_name}" already exists']
				else:
					if table_name == "ex06_movies":
						command = init.sql_command
					else:
						command = f"""
							CREATE TABLE {table_name} (
								title VARCHAR(64) NOT NULL,
								episode_nb INTEGER PRIMARY KEY,
								opening_crawl TEXT,
								director VARCHAR(32) NOT NULL,
								producer VARCHAR(128) NOT NULL,
								release_date DATE NOT NULL
							);
							"""
					try:
						cur.execute(command)
						conn.commit()
						messages = ["OK"]
					except (psycopg2.DatabaseError, Exception) as error:
						conn.rollback()
						messages = [str(error)]

	except Exception as e:
		messages = [str(e)]

	return render(
		request,
		"d05/templates/form.html",
		{
			"title": page_title,
			"label": f"init {table_name} table",
			"messages": messages,
		},
	)


init.sql_commands = {}

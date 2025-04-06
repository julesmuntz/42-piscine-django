from django.shortcuts import render
import psycopg2
from decouple import config
from django.db import connection


def get_db_connection():
	return psycopg2.connect(
		dbname=config("DB_NAME"),
		user=config("DB_USER"),
		password=config("DB_PASSWORD"),
		host=config("DB_HOST"),
		port=config("DB_PORT"),
	)


def init(request, table_name, use_sql, page_title):
	message = "OK"
	try:
		if use_sql:
			with get_db_connection() as conn:
				cur = conn.cursor()
				cur.execute(f"SELECT EXISTS(SELECT relname FROM pg_class WHERE relname='{table_name}')")
				exist = cur.fetchone()[0]
				if not exist:
					message = f'relation "{table_name}" does not exist'
				if request.method == "POST":
					try:
						command = f"""
						CREATE TABLE {table_name} (
							title VARCHAR(64) NOT NULL,
							episode_nb INTEGER PRIMARY KEY,
							opening_crawl TEXT,
							director VARCHAR(32) NOT NULL,
							producer VARCHAR(128) NOT NULL,
							release_date DATE NOT NULL
						)
						"""
						cur.execute(command)
						conn.commit()
						message = "OK"
					except (psycopg2.DatabaseError, Exception) as error:
						conn.rollback()
						message = str(error)
		else:
			with connection.cursor() as cur:
				cur.execute(f"SELECT EXISTS(SELECT relname FROM pg_class WHERE relname='{table_name}')")
				exist = cur.fetchone()[0]
				if not exist:
					message = f'relation "{table_name}" does not exist'
				if request.method == "POST":
					message = "OK"
	except Exception as e:
		message = str(e)

	return render(
		request,
		"d05/templates/form.html",
		{
			"title": page_title,
			"label": f"init {table_name} table",
			"message": message,
		},
	)

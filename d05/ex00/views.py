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
	label = f"init {table_name} table"
	tables = [table_name]
	if hasattr(init, "tables") and table_name in init.tables:
		tables = init.tables[table_name]
		label = f"init {' and '.join(tables)} tables"
	try:
		with get_db_connection() as conn:
			cur = conn.cursor()
			tables_exist = {}
			for table in tables:
				cur.execute(
					f"SELECT EXISTS(SELECT relname FROM pg_class WHERE relname='{table}')"
				)
				tables_exist[table] = cur.fetchone()[0]
			if request.method == "POST":
				existing_tables = [
					f'Table "{table}" already exists'
					for table, exists in tables_exist.items()
					if exists
				]
				if existing_tables:
					messages = existing_tables
				else:
					if hasattr(init, f"{table_name[:4]}_sql"):
						command = getattr(init, f"{table_name[:4]}_sql")
					else:
						command = f"""
							CREATE TABLE {table_name} (
								title VARCHAR(64) NOT NULL UNIQUE,
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
						messages = ["OK"] * len(tables)
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
			"label": label,
			"messages": messages,
		},
	)

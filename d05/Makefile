.PHONY: all run clean-cache clean-venv clean-static clean-migrations clean-db clean-local clean populate-ex09 populate-ex10 populate \
		migrate-ex01 migrate-ex03 migrate-ex05 migrate-ex07 migrate-ex09 migrate-ex10

all: run

run:
	if [ -d "venv" ]; then \
		. venv/bin/activate && \
		python3 -m pip install --upgrade pip && \
		python3 -m pip install --force-reinstall -r requirements.txt && \
		python3 manage.py makemigrations && \
		python3 manage.py collectstatic --noinput --clear -v=0 && \
		python3 manage.py runserver; \
	else \
		python3 -m venv venv && \
		. venv/bin/activate && \
		python3 -m pip install --upgrade pip && \
		python3 -m pip install -r requirements.txt && \
		python3 manage.py makemigrations && \
		python3 manage.py collectstatic --noinput --clear -v=0 && \
		python3 manage.py runserver; \
	fi

migrate-ex01:
	. venv/bin/activate && python3 manage.py migrate ex01

migrate-ex03:
	. venv/bin/activate && python3 manage.py migrate ex03

migrate-ex05:
	. venv/bin/activate && python3 manage.py migrate ex05

migrate-ex07:
	. venv/bin/activate && python3 manage.py migrate ex07

migrate-ex09:
	. venv/bin/activate && python3 manage.py migrate ex09

migrate-ex10:
	. venv/bin/activate && python3 manage.py migrate ex10

migrate: migrate-ex01 migrate-ex03 migrate-ex05 migrate-ex07 migrate-ex09 migrate-ex10

populate-ex09:
	python3 manage.py loaddata d05/static/data/ex09_initial_data.json

populate-ex10:
	python3 manage.py loaddata d05/static/data/ex10_initial_data.json

populate: populate-ex09 populate-ex10

clean-cache:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

clean-venv:
	rm -rf venv

clean-static:
	rm -rf static/

clean-migrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

clean-db: clean-migrations
	python3 -c "import psycopg2; from decouple import config; \
		conn = psycopg2.connect(dbname=config('DB_NAME'), user=config('DB_USER'), \
		password=config('DB_PASSWORD'), host=config('DB_HOST'), port=config('DB_PORT')); \
		cur = conn.cursor(); \
		cur.execute('DROP TABLE IF EXISTS ex00_movies CASCADE'); \
		cur.execute('DROP TABLE IF EXISTS ex01_movies CASCADE'); \
		cur.execute('DROP TABLE IF EXISTS ex02_movies CASCADE'); \
		cur.execute('DROP TABLE IF EXISTS ex03_movies CASCADE'); \
		cur.execute('DROP TABLE IF EXISTS ex04_movies CASCADE'); \
		cur.execute('DROP TABLE IF EXISTS ex05_movies CASCADE'); \
		cur.execute('DROP TABLE IF EXISTS ex06_movies CASCADE'); \
		cur.execute('DROP TABLE IF EXISTS ex07_movies CASCADE'); \
		cur.execute('DROP TABLE IF EXISTS ex08_planets CASCADE'); \
		cur.execute('DROP TABLE IF EXISTS ex08_people CASCADE'); \
		cur.execute('DROP TABLE IF EXISTS ex09_planets CASCADE'); \
		cur.execute('DROP TABLE IF EXISTS ex09_people CASCADE'); \
		cur.execute('DROP TABLE IF EXISTS ex10_planets CASCADE'); \
		cur.execute('DROP TABLE IF EXISTS ex10_people CASCADE'); \
		cur.execute('DROP TABLE IF EXISTS ex10_movies CASCADE'); \
		cur.execute('DROP TABLE IF EXISTS ex10_movies_characters CASCADE'); \
		cur.execute('DELETE FROM django_migrations WHERE app LIKE \'ex%\''); \
		conn.commit(); \
		conn.close();"

clean-local: clean-cache clean-venv clean-static clean-migrations

clean: clean-cache clean-static clean-venv clean-db
.PHONY: all run clean-cache clean-venv clean-static clean-migrations clean-db clean-local clean

all: run

run:
	if [ -d "venv" ]; then \
		. venv/bin/activate && \
		python3 -m pip install --upgrade pip && \
		python3 -m pip install --force-reinstall -r requirements.txt && \
		python3 manage.py makemigrations && \
		python3 manage.py migrate && \
		python3 manage.py collectstatic --noinput --clear -v=0 && \
		python3 manage.py runserver; \
	else \
		python3 -m venv venv && \
		. venv/bin/activate && \
		python3 -m pip install --upgrade pip && \
		python3 -m pip install -r requirements.txt && \
		python3 manage.py makemigrations && \
		python3 manage.py migrate && \
		python3 manage.py collectstatic --noinput --clear -v=0 && \
		python3 manage.py runserver; \
	fi

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
		cur.execute('DELETE FROM django_migrations WHERE app LIKE \'ex%\''); \
		conn.commit(); \
		conn.close();"

clean-local: clean-cache clean-venv clean-static clean-migrations

clean: clean-cache clean-static clean-venv clean-db
.PHONY: all run clean-cache clean-venv clean-static clean-local clean

all: run

run:
	if [ -d "venv" ]; then \
		. venv/bin/activate && \
		python3 -m pip install --upgrade pip && \
		python3 -m pip install -r requirements.txt && \
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

clean-local: clean-cache clean-venv clean-static

clean: clean-cache clean-static clean-venv
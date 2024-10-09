#!/bin/bash

python3 -m venv django_venv
source django_venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip freeze
python3 manage.py runserver
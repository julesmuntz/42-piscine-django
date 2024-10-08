#!/bin/bash

if ! [ -d "d05" ]; then
	echo "Error: the \"d05\" directory does not exist"
	exit 1
fi
python3 -m venv django_venv
source django_venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip freeze
cd d05
python3 manage.py runserver

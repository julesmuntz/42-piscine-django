#!/bin/bash

python3 -m venv django_venv
source django_venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip freeze
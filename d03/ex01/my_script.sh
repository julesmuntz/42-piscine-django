#!/bin/bash

python -m pip --version

python -m pip install git+https://github.com/jaraco/path.git \
	--target=local_lib \
	--upgrade \
	--log local_lib/installation.log

python my_program.py


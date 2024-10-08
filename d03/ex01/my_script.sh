#!/bin/bash

python3 -m pip --version

python3 -m pip install git+https://github.com/jaraco/path \
	--pre \
	--target=local_lib \
	--upgrade \
	--log local_lib/installation.log

python3 my_program.py
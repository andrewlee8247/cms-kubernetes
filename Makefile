setup:
	python3 -m venv ~/.ccdr

install:
	pip3 install -r requiremnts.txt --user

test:
	#python -m pytest -vv --cov=test.py
	#python -m pytest --show-capture=no --nbval notebook.ipynb

lint:
	pylint --disable=R,C test.py

all: install lint test

setup:
	python3 -m venv ~/.ccdr

install:
	pip3 install -r requiremnts.txt --user

test:
	#python -m pytest -vv --cov=app/lib/ test.py
	#python -m pytest --show-capture=no --nbval */**.ipynb

lint:
	pylint --disable=R,C,W0702,W0703 app/**/**.py

all: install lint test

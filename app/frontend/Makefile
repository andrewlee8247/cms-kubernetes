setup:
	python3 -m venv ~/.ccdr

install:
	pip3 install -r requirements.txt --user

test:
	#python -m pytest -vv --cov=lib *.py

lint:
	pylint --disable=R,C,W0703 app.py

all: install lint test

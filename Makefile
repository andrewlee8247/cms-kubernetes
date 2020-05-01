setup:
	python3 -m venv ~/.ccdr

install:
	pip3 install -r requirements.txt --user

test:
	python -m pytest -vv --cov=app/api/lib tests/*.py

lint:
	pylint --disable=R,C,W0702,W0703,E1101,E0213,W0104,W0642,W1202 app/**/**/**.py

all: install lint test

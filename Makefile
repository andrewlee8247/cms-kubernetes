setup:
	python3 -m venv ~/.ccdr

install:
	pip3 install -r requiremnts.txt --user

test:
	#python -m pytest -vv --cov=api/lib tests/*.py

lint:
	pylint --disable=R,C,W0702,W0703,E1101,E0213,W0104,W0642 api/**/**.py

all: install lint test

setup:
	python3 -m venv ~/.ccdr

install:
	pip3 install -r requiremnts.txt --user

test:
	#python -m pytest -vv --cov=lib/ *.py

lint:
	pylint --disable=R,C,W0702,W0703 */**.py

all: install lint test

install:
	pip install --upgrade pip &&\
		pip install -r requirement.txt
lint:
	pylint --disable=R,C main.py

test:
	python -m pytest -vv test_main.py

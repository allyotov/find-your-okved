run:
	python -m src

test:
	python -m pytest


test.github_client:
	python -m pytest tests/integrational/test_github_client.py -vvv
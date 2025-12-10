run:
	python -m src

test:
	python -m pytest


test.github_client:
	python -m pytest tests/integrational/test_github_client.py -vvv


test.cache_repo:
	python -m pytest tests/integrational/test_cache_repo.py -vvv


test.okved_service:
	python -m pytest tests/unit/services/test_okved.py


test.view:
	python -m pytest tests/unit/views/test_form_resulting_message.py
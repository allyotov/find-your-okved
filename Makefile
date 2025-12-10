run:
	python -m src $(phone)

help:
	python -m src --help

test:
	python -m pytest


test.github_client:
	python -m pytest tests/unit/clients/test_github_client.py -vvv


test.github_client.get_new_etag:
	python -m pytest tests/unit/clients/test_github_client.py::test_get_new_okved_json_etag


test.github_client.check_etag:
	python -m pytest tests/unit/clients/test_github_client.py::test_check_actual_okved_json_etag


test.github_client.get_okveds:
	python -m pytest tests/unit/clients/test_github_client.py::test_get_new_okved_json


test.cache_repo:
	python -m pytest tests/integrational/test_cache_repo.py -vvv


test.okved_service:
	python -m pytest tests/unit/services/test_okved.py


test.view:
	python -m pytest tests/unit/views/test_form_resulting_message.py


test.prefer_complete_merge:
	python -m pytest tests/unit/services/test_okved.py::test_find_matching_okved_code__prefer_complete_match
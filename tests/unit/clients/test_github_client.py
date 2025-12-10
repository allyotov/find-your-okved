import base64
import json
from unittest.mock import patch

import httpx
import pytest

from src.clients.github import GithubClient


@pytest.fixture
def mock_httpx_client_head():
    with patch('src.clients.github.httpx_client.head') as mock:
        yield mock


@pytest.fixture
def mock_httpx_client_get():
    with patch('src.clients.github.httpx_client.get') as mock:
        yield mock


@pytest.fixture
def github_client() -> GithubClient:
    return GithubClient(owner='test_owner', repo='test_case_repo', file_path='okveds.json')


def test_get_new_okved_json_etag(github_client, mock_httpx_client_head):
    mock_httpx_client_head.return_value = httpx.Response(200, headers={'ETag': 'test_etag_string'})
    etag = github_client.check_okved_json_etag(cached_etag=None)
    assert etag
    assert etag == 'test_etag_string'


def test_check_actual_okved_json_etag(github_client, mock_httpx_client_head):
    mock_httpx_client_head.return_value = httpx.Response(304, headers={})
    cached_etag = 'test_etag_string'
    check_result = github_client.check_okved_json_etag(cached_etag=cached_etag)
    assert check_result is None


def test_get_new_okved_json(github_client, mock_httpx_client_get):
    okveds_list = [{'code': 123, 'name': 'abc', 'items': []}]
    okveds_encoded_bytes = _get_encoded_bytes_from_list(okveds_list)
    mock_httpx_client_get.return_value = httpx.Response(200, json={'content': okveds_encoded_bytes})
    okved_codes = github_client.load_okved_json()

    assert okved_codes == okveds_list


def _get_encoded_bytes_from_list(given_list: list[dict]) -> str:
    okveds_json_string = json.dumps(given_list)
    bytes_string = okveds_json_string.encode('utf-8')
    return base64.b64encode(bytes_string).decode('ascii')


# TODO: добавить тесты, проверяющие случаи, когда методы .get() и .head() httpx.Client завершаются неудачно, поднимая
# исключения.

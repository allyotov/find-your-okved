import pytest

from src.clients.github import GithubClient
from src.settings import GITHUB_SETTINGS

# TODO: необходимо написать фикстуру, которая будет возвращать mock httpx клиента github API, поскольку мы не должны
# проверять в своих модульных тестах работу стороннего API;


@pytest.fixture
def github_client() -> GithubClient:
    return GithubClient(owner=GITHUB_SETTINGS.owner, repo=GITHUB_SETTINGS.repo, file_path=GITHUB_SETTINGS.file_path)


def test_get_new_okved_json_etag(github_client):
    etag = github_client.check_okved_json_etag(cached_etag=None)
    assert etag
    assert type(etag) is str


def test_check_actual_okved_json_etag(github_client):
    cached_etag = github_client.check_okved_json_etag(cached_etag=None)
    check_result = github_client.check_okved_json_etag(cached_etag=cached_etag)
    assert check_result is None


def test_get_new_okved_json(github_client):
    okved_codes = github_client.load_okved_json()
    assert type(okved_codes) is list

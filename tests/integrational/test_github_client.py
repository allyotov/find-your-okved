import pytest

from src.clients.github import GithubClient
from src.settings import GITHUB_SETTINGS


@pytest.fixture
def github_client() -> GithubClient:
    return GithubClient(owner=GITHUB_SETTINGS.owner, repo=GITHUB_SETTINGS.repo, file_path=GITHUB_SETTINGS.file_path)


def test_get_okved_json_metadata__gets_etag_as_str(github_client):
    date_str = github_client.get_github_file_metadata()
    assert type(date_str) is str

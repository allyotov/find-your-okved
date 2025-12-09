from src.clients.github import GithubClient
from src.settings import GITHUB_SETTINGS


def get_github_client() -> GithubClient:
    return GithubClient(owner=GITHUB_SETTINGS.owner, repo=GITHUB_SETTINGS.repo, file_path=GITHUB_SETTINGS.file_path)

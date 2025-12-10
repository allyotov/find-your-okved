from src.clients.github import GithubClient
from src.repositories.cache import CacheRepository
from src.services.okved import OkvedService
from src.settings import CACHE_SETTINGS, GITHUB_SETTINGS


def get_github_client() -> GithubClient:
    return GithubClient(owner=GITHUB_SETTINGS.owner, repo=GITHUB_SETTINGS.repo, file_path=GITHUB_SETTINGS.file_path)


def get_cache_repo() -> CacheRepository:
    return CacheRepository(
        etag_cache_path=CACHE_SETTINGS.etag_cache_path,
        okved_json_cache_path=CACHE_SETTINGS.okved_json_cache_path,
    )


def get_okved_service() -> OkvedService:
    github_client = get_github_client()
    cache_repo = get_cache_repo()
    return OkvedService(github_client=github_client, cache_repo=cache_repo)

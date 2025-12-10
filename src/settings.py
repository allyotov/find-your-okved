from pydantic import BaseModel
from pyhocon import ConfigFactory

github_config = ConfigFactory.parse_file('settings/github.conf')
cache_config = ConfigFactory.parse_file('settings/cache.conf')


class GithubSettings(BaseModel):
    owner: str = github_config['config']['owner']
    repo: str = github_config['config']['repo']
    file_path: str = github_config['config']['file_path']


class CacheSettings(BaseModel):
    etag_cache_path: str = cache_config['config']['etag_cache_path']
    okved_json_cache_path: str = cache_config['config']['okved_json_cache_path']


GITHUB_SETTINGS = GithubSettings()
CACHE_SETTINGS = CacheSettings()

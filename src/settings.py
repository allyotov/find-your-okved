from pydantic import BaseModel
from pyhocon import ConfigFactory

github_config = ConfigFactory.parse_file('settings/github.conf')


class GithubSettings(BaseModel):
    owner: str = github_config['config']['owner']
    repo: str = github_config['config']['repo']
    file_path: str = github_config['config']['file_path']


GITHUB_SETTINGS = GithubSettings()

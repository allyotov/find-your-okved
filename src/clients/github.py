import logging

from httpx import Client

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


OKVED_JSON_GITHUB_URL_TEMPLATE = 'https://api.github.com/repos/{owner}/{repo}/contents/{file_path}'


class GithubClient:
    def __init__(self, owner: str, repo: str, file_path: str) -> None:
        self._http_client = Client()
        self._owner: str = owner
        self._repo: str = repo
        self._file_path: str = file_path

    def get_github_file_metadata(
        self,
    ) -> dict | None:
        url = OKVED_JSON_GITHUB_URL_TEMPLATE.format(owner=self._owner, repo=self._repo, file_path=self._file_path)

        headers = {'Accept': 'application/vnd.github.v3+json'}

        # if token:
        #     headers['Authorization'] = f'token {token}'

        with self._http_client as client:
            response = client.head(url, headers=headers, follow_redirects=True)

            if response.status_code == 200:
                return response.headers.get('etag')
            else:
                pass

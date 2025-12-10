import base64
import json
import logging

from httpx import Client as httpx_client

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


OKVED_JSON_GITHUB_URL_TEMPLATE = 'https://api.github.com/repos/{owner}/{repo}/contents/{file_path}'


class GithubClient:
    def __init__(self, owner: str, repo: str, file_path: str) -> None:
        self._owner: str = owner
        self._repo: str = repo
        self._file_path: str = file_path

    def check_okved_json_etag(self, cached_etag: str | None = None) -> dict | None:
        url = OKVED_JSON_GITHUB_URL_TEMPLATE.format(owner=self._owner, repo=self._repo, file_path=self._file_path)

        headers = {'Accept': 'application/vnd.github.v3+json'}

        if cached_etag:
            headers['If-None-Match'] = cached_etag

        with httpx_client() as client:
            # TODO: добавить обработку исключений запроса;
            response = client.head(url, headers=headers, follow_redirects=True)

        if response.status_code == 304:
            logger.info("etag didn't change.")
        elif response.status_code == 200:
            logger.info('etag updated.')
            new_etag = response.headers.get('ETag')
            if new_etag:
                return new_etag
        else:
            logger.warning('Check github okved.json etag failed: %s - %s', response.status_code, response.text)

        return None

    def load_okved_json(self) -> list | None:
        url = OKVED_JSON_GITHUB_URL_TEMPLATE.format(owner=self._owner, repo=self._repo, file_path=self._file_path)

        headers = {'Accept': 'application/vnd.github.v3+json'}

        with httpx_client() as client:
            # TODO: добавить обработку исключений запроса;
            response = client.get(url, headers=headers)

        okved_codes = None

        if response.status_code == 200:
            content = response.json()['content']
            decoded = base64.b64decode(content).decode('utf-8')
            okved_codes = json.loads(decoded)
        else:
            logger.warning('Loading github okved.json failed: %s - %s', response.status_code, response.text)

        return okved_codes

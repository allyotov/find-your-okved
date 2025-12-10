import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class CacheRepository:
    def __init__(self, etag_cache_path: str, okved_json_cache_path: str):
        self._etag_cache_path = etag_cache_path
        self._okved_json_cache_path = okved_json_cache_path

    def get_okved_json_etag_from_cache(self) -> str | None:
        cache = Path(self._etag_cache_path)
        saved_etag = None
        if not cache.exists():
            return saved_etag

        try:
            cache_data = json.loads(cache.read_text())
        except json.JSONDecodeError as exc:
            logger.warning(exc)
            return saved_etag
        try:
            saved_etag = cache_data.get('etag')
        except KeyError as exc:
            logger.warning(exc)

        return saved_etag

    def save_okved_json_etag_to_cache(self, etag: str) -> None:
        pass

    def save_okved_json_to_cache(self) -> None:
        pass

    def get_okved_json_from_cache(self) -> dict:
        pass

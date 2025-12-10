import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class CantSaveJsonError(Exception): ...


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
        file_path = Path(self._etag_cache_path)

        data = {'etag': etag}

        _try_save_json(file_path=file_path, data=data)

    def save_okved_codes_to_cache(self, new_okved_codes: list) -> None:
        file_path = Path(self._okved_json_cache_path)

        _try_save_json(file_path=file_path, data=new_okved_codes)

    def get_okved_code_from_cache(self) -> list:
        pass


def _try_save_json(file_path: Path, data: dict[str, str]) -> None:
    try:
        with file_path.open('w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as exc:  # TODO: уточнить конкретный тип возможного исключения
        logger.error(exc)
        raise CantSaveJsonError()

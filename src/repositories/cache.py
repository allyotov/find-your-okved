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

    def get_okved_codes_from_cache(self) -> list[dict] | None:
        cache = Path(self._okved_json_cache_path)
        okved_codes = None
        if not cache.exists():
            return okved_codes

        try:
            okved_codes = json.loads(cache.read_text())
        except json.JSONDecodeError as exc:
            logger.warning(exc)
            return okved_codes

        if type(okved_codes) is not list:
            logger.warning('Wrong format of okved file cache')
            okved_codes = None

        return okved_codes


def _try_save_json(file_path: Path, data: dict[str, str]) -> None:
    try:
        with file_path.open('w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as exc:  # TODO: уточнить конкретный тип возможного исключения
        logger.error(exc)
        raise CantSaveJsonError()

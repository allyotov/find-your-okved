import json
from pathlib import Path

import pytest

from src.repositories.cache import CacheRepository

TEST_ETAG_CACHE_PATH = 'test_etag_cache.json'
TEST_OKVED_JSON_PATH = 'test_okved.json'
TEST_CACHED_ETAG = 'test_etag_str'


@pytest.fixture
def cache_repo():
    return CacheRepository(etag_cache_path=TEST_ETAG_CACHE_PATH, okved_json_cache_path=TEST_OKVED_JSON_PATH)


@pytest.fixture
def correct_etag_json_file():
    file_path = Path(TEST_ETAG_CACHE_PATH)

    data = {'etag': TEST_CACHED_ETAG}
    with file_path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    yield file_path

    if file_path.exists():
        file_path.unlink()


@pytest.fixture
def invalid_etag_json_file():
    file_path = Path(TEST_ETAG_CACHE_PATH)

    # Записываем заведомо некорректный JSON
    invalid_content = """{
        "etag": "test_etag"
    """  # Отсутствует закрывающая скобка

    with file_path.open('w', encoding='utf-8') as f:
        f.write(invalid_content)

    yield file_path

    if file_path.exists():
        file_path.unlink()


@pytest.fixture
def wrong_key_etag_json_file():
    file_path = Path(TEST_ETAG_CACHE_PATH)

    data = {'_e_tag_': TEST_CACHED_ETAG}
    with file_path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    yield file_path

    if file_path.exists():
        file_path.unlink()


@pytest.fixture
def okved_codes():
    return [
        {
            'code': 'Раздел A',
            'name': 'Сельское, лесное хозяйство, охота, рыболовство и рыбоводство',
            'items': [],
        },
        {
            'code': 'Раздел Б',
            'name': '...',
            'items': [],
        },
    ]


@pytest.fixture
def correct_okved_json_file(okved_codes):
    file_path = Path(TEST_OKVED_JSON_PATH)

    with file_path.open('w', encoding='utf-8') as f:
        json.dump(okved_codes, f, ensure_ascii=False, indent=2)
    yield file_path

    if file_path.exists():
        file_path.unlink()


@pytest.fixture
def invalid_okved_json_file():
    file_path = Path(TEST_OKVED_JSON_PATH)

    # Записываем заведомо некорректный JSON
    invalid_content = """
        [
    """  # Отсутствует содержимое после открывающей квадратной скобки

    with file_path.open('w', encoding='utf-8') as f:
        f.write(invalid_content)

    yield file_path

    if file_path.exists():
        file_path.unlink()


@pytest.fixture
def no_list_in_okved_json_file():
    file_path = Path(TEST_OKVED_JSON_PATH)

    data = {'_some_key_': {'_some_nested_key_': '_some_item_value_'}}
    with file_path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    yield file_path

    if file_path.exists():
        file_path.unlink()


def test_load_etag__file_exists__returns_etag(cache_repo, correct_etag_json_file):
    assert cache_repo.get_okved_json_etag_from_cache() == TEST_CACHED_ETAG


def test_load_etag__file_doesnt_exists__returns_none(cache_repo):
    assert cache_repo.get_okved_json_etag_from_cache() is None


def test_load_etag__invalid_file__returns_none(cache_repo, invalid_etag_json_file):
    assert cache_repo.get_okved_json_etag_from_cache() is None


def test_load_etag__no_etag_key__returns_none(cache_repo, wrong_key_etag_json_file):
    assert cache_repo.get_okved_json_etag_from_cache() is None


def test_save_etag__resulting_file_exists(cache_repo):
    cache_repo.save_okved_json_etag_to_cache(etag=TEST_CACHED_ETAG)

    file_path = Path(TEST_ETAG_CACHE_PATH)

    assert file_path.exists()

    if file_path.exists():
        file_path.unlink()


def test_save_etag__valid_resulting_file(cache_repo):
    cache_repo.save_okved_json_etag_to_cache(etag=TEST_CACHED_ETAG)

    file_path = Path(TEST_ETAG_CACHE_PATH)

    cache_data = json.loads(file_path.read_text())

    assert 'etag' in cache_data
    assert type(cache_data['etag']) is str

    if file_path.exists():
        file_path.unlink()


# TODO: написать тесты, отражающие неуспешные кейсы сохранения etag в файл: ошибка сохранения в файл,
# неправильный формат переданных данных;


def test_save_okved_codes__resulting_file_exists(cache_repo, okved_codes):
    cache_repo.save_okved_codes_to_cache(new_okved_codes=okved_codes)

    file_path = Path(TEST_OKVED_JSON_PATH)

    assert file_path.exists()

    if file_path.exists():
        file_path.unlink()


def test_save_okved_codes__valid_resulting_file(cache_repo, okved_codes):
    cache_repo.save_okved_codes_to_cache(new_okved_codes=okved_codes)

    file_path = Path(TEST_OKVED_JSON_PATH)

    cache_data = json.loads(file_path.read_text())

    assert cache_data == okved_codes

    if file_path.exists():
        file_path.unlink()


# TODO: написать тесты, отражающие неуспешные кейсы сохранения ОКВЭД в файл: ошибка сохранения в файл,
# неправильный формат переданных данных;


def test_load_okved_codes__file_exists__returns_etag(cache_repo, correct_okved_json_file, okved_codes):
    assert cache_repo.get_okved_codes_from_cache() == okved_codes


def test_load_okved_codes__file_doesnt_exists__returns_none(cache_repo):
    assert cache_repo.get_okved_codes_from_cache() is None


def test_load_okved_codes__invalid_file__returns_none(cache_repo, invalid_okved_json_file):
    assert cache_repo.get_okved_codes_from_cache() is None


def test_load_okved_codes__no_list_in_content__returns_none(cache_repo, no_list_in_okved_json_file):
    assert cache_repo.get_okved_codes_from_cache() is None

import logging
from typing import Tuple

from src.clients.github import GithubClient
from src.repositories.cache import CacheRepository, CantSaveJsonError

logger = logging.getLogger('okved_service')
logging.basicConfig(level=logging.DEBUG)

PHONE_NUMBER_LEN = 11


class PhoneNumberFormatError(ValueError): ...


class WrongDigitsNumberError(PhoneNumberFormatError):
    def __init__(self, digits_number: int):
        self.digits_number = digits_number
        message = 'Wrong digits number in the phone: {number}'.format(number=digits_number)
        super().__init__(message)


class WrongCountryCodeError(PhoneNumberFormatError):
    def __init__(self, country_code: str, plus: bool = False):
        self.contry_code = country_code
        plus_prefix = ''
        if plus:
            plus_prefix = '+'
        message = 'Wrong country code in the phone: {plus}{code}'.format(plus=plus_prefix, code=country_code)
        super().__init__(message)


class WrongSecondDigitError(PhoneNumberFormatError):
    def __init__(self, second_digit: str):
        self.second_digit = second_digit
        message = 'Wrong second digit in the phone: {digit}'.format(digit=second_digit)
        super().__init__(message)


class EmptyPhoneNumberError(PhoneNumberFormatError):
    def __init__(self):
        message = 'Given phone number is empty'
        super().__init__(message)


class OkvedService:
    def __init__(self, github_client: GithubClient, cache_repo: CacheRepository):
        self._github_client = github_client
        self._cache_repo = cache_repo

    def get_okved(self, raw_phone_number: str) -> Tuple[str | None, dict | None, str]:
        error_message = ''
        normalized_phone, error_message = try_normalize_phone(raw_phone_number)
        if not normalized_phone:
            return normalized_phone, None, error_message
        okved_code = self.get_okved_by_phone(phone=normalized_phone)
        return normalized_phone, okved_code, error_message

    def get_okved_by_phone(self, phone: str) -> dict | None:
        okved_codes = self._get_actual_okved_codes()
        if not okved_codes:
            return None
        return find_matching_okved_code(phone=phone, okved_codes=okved_codes)

    def _get_actual_okved_codes(self) -> list[dict] | None:
        cached_json_etag = self._cache_repo.get_okved_json_etag_from_cache()
        logger.info('Проверяем актуальность ОКВЭД в локальном кэше по etag...')
        new_etag = self._github_client.check_okved_json_etag(cached_etag=cached_json_etag)

        new_okved_codes = None
        if new_etag:
            logger.info('Локальные ОКВЭД устарели, обновляем etag и ОКВЭД...')
            self._cache_repo.save_okved_json_etag_to_cache(etag=new_etag)
            new_okved_codes = self._github_client.load_okved_json()
        else:
            logger.info('локальные ОКВЭД актуальны, используем их...')

        if new_okved_codes:
            try:
                self._cache_repo.save_okved_codes_to_cache(new_okved_codes=new_okved_codes)
            except CantSaveJsonError:
                logger.warning('Не удалось сохранить новые ОКВЭД в кэш;')
            return new_okved_codes

        okved_codes_from_cache = self._cache_repo.get_okved_codes_from_cache()

        if not okved_codes_from_cache:
            logger.warning('Не удалось загрузить ОКВЭД из кэша, загружаем их заново из реестра...')
            new_okved_codes = self._github_client.load_okved_json()
            self._cache_repo.save_okved_codes_to_cache(new_okved_codes=new_okved_codes)
            return new_okved_codes
        return okved_codes_from_cache


def try_normalize_phone(raw_phone_number: str):
    normalized_phone = False
    error_message = ''
    try:
        normalized_phone = normalize_phone(sequence=raw_phone_number)
    except EmptyPhoneNumberError:
        error_message = 'Данный телефонный номер пуст'
    except WrongDigitsNumberError as dig_number_error:
        error_message = 'В данном телефонном номере неправильное число цифр ({actual} вместо {needed})'.format(
            actual=dig_number_error.digits_number,
            needed=PHONE_NUMBER_LEN,
        )
    except WrongCountryCodeError as country_code_error:
        error_message = 'В данном телефонном номере неправильный код страны ({actual} вместо +7 или 8)'.format(
            actual=country_code_error.contry_code,
        )
    except WrongSecondDigitError as second_digit_error:
        error_message = 'В данном телефонном номере неправильная вторая цифра ({actual} вместо 9)'.format(
            actual=second_digit_error.second_digit,
        )
    return normalized_phone, error_message


def normalize_phone(sequence: str) -> str | bool:
    """
    Нормализует российский мобильный номер до формата +79XXXXXXXXX.

    Args:
        input_str (str): входная строка с номером (любой формат)

    Returns:
        str or False: нормализованный номер или False при ошибке
    """
    _validate_phone_not_empty(sequence=sequence)

    plus_before_first_digit, digits = _parse_raw_phone(raw_phone=sequence)

    _validate_digits_number(digits)

    _validate_country_code(digits, plus_before_first_digit)

    _validate_second_digit(digits)

    normalized = '+7{rest_digits}'.format(rest_digits=digits[1:])

    return normalized


def _parse_raw_phone(raw_phone: str) -> Tuple[bool, str]:
    digits = []
    plus_before_first_digit = False
    first_digit_found = False

    for char in raw_phone:
        if char == '+' and not first_digit_found:
            plus_before_first_digit = True
        elif char.isdigit():
            if not first_digit_found and char == '0':
                continue
            digits.append(char)
            first_digit_found = True

    return plus_before_first_digit, ''.join(digits)


def _validate_phone_not_empty(sequence: str) -> None:
    if not sequence:
        raise EmptyPhoneNumberError()


def _validate_digits_number(digits: str) -> None:
    digits_number = len(digits)
    if digits_number != PHONE_NUMBER_LEN:
        raise WrongDigitsNumberError(digits_number=digits_number)


def _validate_country_code(digits: str, plus_before_first_digit) -> None:
    country_code = digits[0]
    if country_code != '7' and plus_before_first_digit:
        raise WrongCountryCodeError(country_code=country_code, plus=True)

    if country_code != '8' and not plus_before_first_digit:
        raise WrongCountryCodeError(country_code=country_code, plus=False)


def _validate_second_digit(digits: str) -> None:
    second_digit = digits[1]
    if second_digit != '9':
        raise WrongSecondDigitError(second_digit=second_digit)


def find_matching_okved_code(phone: str, okved_codes: list[dict]) -> dict[str, str | int | bool]:
    max_match_len = -1  # В случае, если совпадений будет не найдено, возвратится первый непустой ОКВЭД;
    longest_match_code = ''
    longest_match_code_title = ''

    complete_match_found = False

    nodes = []
    for section in okved_codes:
        nodes.extend(section['items'])

    while nodes:
        next_nodes = []
        for node in nodes:
            if 'items' in node:
                next_nodes.extend(node['items'])
            code_as_is = node['code']
            code_as_digits = _get_digits_of_code_if_correct(code_as_is)
            matches_count, complete_match = _compare_code_with_phone(code=code_as_digits, phone=phone)

            if complete_match_found and not complete_match:
                continue
            elif not complete_match_found and complete_match:
                max_match_len = matches_count
                longest_match_code = code_as_is
                longest_match_code_title = node['name']

                complete_match_found = True

            elif (not complete_match_found and not complete_match) or (complete_match_found and complete_match):
                if matches_count > max_match_len:
                    max_match_len = matches_count
                    longest_match_code = code_as_is
                    longest_match_code_title = node['name']

        nodes = next_nodes

    return {
        'okved': longest_match_code,
        'matches_count': max_match_len,
        'complete_match': complete_match_found,
        'title': longest_match_code_title,
    }


def _get_digits_of_code_if_correct(okved_code: str) -> str:
    digits = []
    for char in okved_code:
        if char.isalpha():
            return ''
        if char.isdigit():
            digits.append(char)
    return ''.join(digits)


def _compare_code_with_phone(code: str, phone: str) -> Tuple[int, bool]:
    if not code:
        return 0, False

    code_len = len(code)
    phone_end = phone[-code_len:]
    if code == phone_end:
        return code_len, True
    else:
        trailing_matches_count = 0
        for code_digit, phone_digit in zip(code, phone_end):
            if code_digit == phone_digit:
                trailing_matches_count += 1
        return trailing_matches_count, False

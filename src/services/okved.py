from typing import Tuple


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
    def __init__(self):
        pass

    def get_okved(self, raw_phone_number: str) -> Tuple[str | bool, str]:
        error_message = ''
        normalized_phone, error_message = try_normalize_phone(raw_phone_number)
        if not normalize_phone:
            return normalized_phone, error_message
        return self.get_okved_by_phone(phone=normalized_phone), error_message

    def get_okved_by_phone(self, phone: str) -> str:
        return '0.0.0.0'


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
            needed=11,
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
            digits.append(char)
            first_digit_found = True

    return plus_before_first_digit, ''.join(digits)


def _validate_phone_not_empty(sequence: str) -> None:
    if not sequence:
        raise EmptyPhoneNumberError()


def _validate_digits_number(digits: str) -> None:
    digits_number = len(digits)
    if digits_number != 11:
        raise WrongDigitsNumberError(digits_number=digits_number)


def _validate_country_code(digits: str, plus_before_first_digit) -> None:
    country_code = digits[0]
    if country_code != '7' and plus_before_first_digit:
        raise WrongCountryCodeError(country_code=country_code, plus=True)


def _validate_second_digit(digits: str) -> None:
    second_digit = digits[1]
    if second_digit != '9':
        raise WrongSecondDigitError(second_digit=second_digit)

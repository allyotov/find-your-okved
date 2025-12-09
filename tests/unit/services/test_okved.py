import pytest

from src.services.okved import (
    EmptyPhoneNumberError,
    WrongCountryCodeError,
    WrongDigitsNumberError,
    WrongSecondDigitError,
    normalize_phone,
)


@pytest.mark.parametrize(
    'input_sequence',
    [
        '+79001234567',
        '89001234567',
        '+7 (900) 123-45-67',
        '8-900-123-45-67',
        'фываф+фыва7-900-123-45-67',
        'sdfgsdfg8-asdffasdf90A0-asdfffDasdf123asasdf-4##5asdfasdff-67fdgsdfg',
    ],
)
def test_normalize_phone__normalizes_correct_input_sequences(input_sequence):
    result = normalize_phone(sequence=input_sequence)
    assert type(result) is str
    assert result[:3] == '+79'


@pytest.mark.parametrize(
    'input_sequence',
    [
        '',
        None,
    ],
)
def test_normalize_phone__empty_phone__raises_corresponding_error(input_sequence):
    with pytest.raises(EmptyPhoneNumberError):
        normalize_phone(sequence=input_sequence)


@pytest.mark.parametrize(
    'input_sequence',
    [
        '9001234567',
        'abc+7def9ghij',
        '900123456700000000000000000000000000',
        'abc+7def9ghij11111111111111111112341',
    ],
)
def test_normalize_phone__wrong_digits_number__raises_corresponding_error(input_sequence):
    with pytest.raises(WrongDigitsNumberError):
        normalize_phone(sequence=input_sequence)


@pytest.mark.parametrize(
    'input_sequence',
    [
        '+19001234567',
        '+29001234567',
        '+89001234567',
        '99001234567',
        '79001234567',  # Cчитаем, что если перед первой цифрой в строке нет плюса, значит, первой цифрой должна быть 8.
    ],
)
def test_normalize_phone__wrong_country_code__raises_corresponding_error(input_sequence):
    with pytest.raises(WrongCountryCodeError):
        normalize_phone(sequence=input_sequence)


@pytest.mark.parametrize(
    'input_sequence',
    [
        '+71001234567',
        '+72001234567',
        '+73001234567',
        '84001234567',
    ],
)
def test_normalize_phone__wrong_second_digit__raises_corresponding_error(input_sequence):
    with pytest.raises(WrongSecondDigitError):
        normalize_phone(sequence=input_sequence)

import pytest

from src.services.okved import (
    EmptyPhoneNumberError,
    WrongCountryCodeError,
    WrongDigitsNumberError,
    WrongSecondDigitError,
    _compare_code_with_phone,
    find_matching_okved_code,
    normalize_phone,
)


@pytest.mark.parametrize(
    'input_sequence',
    [
        '+79001234567',
        '00000+79001234567',
        '+0000079001234567',
        '000000+0000079001234567',
        '89001234567',
        '00000089001234567',
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
    ],
)
def test_normalize_phone__plus_not_7__raises_wrong_country_code(input_sequence):
    with pytest.raises(WrongCountryCodeError):
        normalize_phone(sequence=input_sequence)


@pytest.mark.parametrize(
    'input_sequence',
    [
        '99001234567',
        '79001234567',  # Cчитаем, что если перед первой цифрой в строке нет плюса, значит, первой цифрой должна быть 8.
    ],
)
def test_normalize_phone__no_plus_not_8_raises_wrong_country_code(input_sequence):
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


def test_find_matching_okved_code__prefer_complete_match():
    phone = '+79001234567'

    okved_codes = [
        {
            'code': 'Раздел 1',
            'items': [{'code': '81.23.45.67', 'name': 'Разведение гуппи Эндлера', 'items': []}],
        },
        {
            'code': 'Раздел 2',
            'items': [
                {
                    'code': '5.67',
                    'name': 'Разведение сомов анциструсов',
                    'items': [],
                },
            ],
        },
    ]

    matching_okved = find_matching_okved_code(phone=phone, okved_codes=okved_codes)
    assert matching_okved == {
        'okved': '5.67',
        'matches_count': 3,
        'complete_match': True,
        'title': 'Разведение сомов анциструсов',
    }


def test_find_matching_okved_code__no_complete_matches__prefer_longest_incomplete():
    phone = '+79001234567'

    okved_codes = [
        {
            'code': 'Раздел 1',
            'items': [{'code': '81.23.45.67', 'name': 'Разведение гуппи Эндлера', 'items': []}],
        },
        {
            'code': 'Раздел 2',
            'items': [
                {
                    'code': '2.67',
                    'name': 'Разведение сомов анциструсов',
                    'items': [],
                },
            ],
        },
    ]

    matching_okved = find_matching_okved_code(phone=phone, okved_codes=okved_codes)
    assert matching_okved == {
        'okved': '81.23.45.67',
        'matches_count': 7,
        'complete_match': False,
        'title': 'Разведение гуппи Эндлера',
    }


def test_find_matching_okved_code__no_matches__return_first_not_empty_code():
    phone = '+79001234567'

    okved_codes = [
        {
            'code': 'Раздел 1',
            'items': [{'code': '80.00.77.70', 'name': 'Разведение гуппи Эндлера', 'items': []}],
        },
        {
            'code': 'Раздел 2',
            'items': [
                {
                    'code': '7.70',
                    'name': 'Разведение сомов анциструсов',
                    'items': [],
                },
            ],
        },
    ]

    matching_okved = find_matching_okved_code(phone=phone, okved_codes=okved_codes)
    assert matching_okved == {
        'okved': '80.00.77.70',
        'matches_count': 0,
        'complete_match': False,
        'title': 'Разведение гуппи Эндлера',
    }


def test_find_matching_okved_code__successfully_processes_nodes_with_no_nested_items():
    phone = '+79001234567'

    okved_codes = [
        {
            'code': 'Раздел 1',
            'items': [{'code': '81.23.45.60', 'name': 'Разведение гуппи Эндлера'}],
        },
        {
            'code': 'Раздел 2',
            'items': [
                {
                    'code': '2.60',
                    'name': 'Разведение сомов анциструсов',
                },
            ],
        },
    ]
    result = find_matching_okved_code(phone=phone, okved_codes=okved_codes)
    assert result


def test_compare_code_with_phone__middle_digits_match__return_matches_count_not_complete_match():
    assert _compare_code_with_phone(phone='+79001234567', code='0560') == (2, False)


def test_compare_code_with_phone__middle_digits_match_last_digits_differ__return_not_zero_matches_not_complete_match():
    assert _compare_code_with_phone(phone='+79001234567', code='1234560') == (6, False)


def test_compare_code_with_phone__all_code_digits_match__return_matches_count_complete_match():
    assert _compare_code_with_phone(phone='+79001234567', code='1234567') == (7, True)

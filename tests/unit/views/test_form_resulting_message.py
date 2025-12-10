from src.commands.cli import form_resulting_message


def test__no_normalized_phone__phone_error_message():
    msg = form_resulting_message(False, None, 'В данном телефонном номере неправильный код страны (0 вместо +7 или 8)')
    assert msg == (
        'Произошла ошибка нормализации телефонного номера:\n'
        'В данном телефонном номере неправильный код страны (0 вместо +7 или 8);'
    )


def test__complete_match_found__show_corresponding_message():
    phone = '+79001234567'
    okved_data = {
        'okved': '5.67',
        'matches_count': 3,
        'complete_match': True,
        'title': 'Разведение сомов анциструсов',
    }
    msg = form_resulting_message(phone, okved_data, '')
    assert msg == (
        'Найден ОКВЭД, все цифры которого (3) совпадают с концевыми цифрами номера.\n'
        'ОКВЭД: 5.67;\n'
        'Название: Разведение сомов анциструсов.\n'
    )


def test__none_okved_data__show_okved_loading_failed_messag():
    phone = '+79001234567'
    okved_data = None
    msg = form_resulting_message(phone, okved_data, '')
    assert msg == (
        'Увы. Нам не удалось загрузить коды ОКВЭД ни из удалённого реестра, ни из локального кэша.\n'
        'Пожалуйста, попробуйте повторить свой запрос чуть позже.'
    )

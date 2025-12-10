import logging

import typer

from src.deps import get_okved_service

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = typer.Typer()

GREETINGS_TEMPLATE = """Вас приветствует утилита "Найди свой ОКВЭД по номеру телефона".
'Вы передали номер телефона: {phone}"""

PHONE_NORMALIZATION_ERROR_TMP = 'Произошла ошибка нормализации телефонного номера:\n{phone_err};'

COMPLETE_MATCH_MSG_TEMPLATE = """Найден ОКВЭД, все цифры которого ({code_len}) совпадают с концевыми цифрами номера.
ОКВЭД: {code};
Название: {title}.
"""

INCOMPLETE_MATCH_MSG_TEMPLATE = """Длина наибольшего совпадения {code_len} цифр.
Соответствующий код такой:
ОКВЭД: {code};
Название: {title}.
"""

NO_MATCH_MSG_TEMPLATE = """Не найдено ни одного совпадающего ОКВЭД.
Первый непустой ОКВЭД такой:
ОКВЭД: {code};
Название: {title}.
"""

OKVED_LOAD_FAILED_MSG = """Увы. Нам не удалось загрузить коды ОКВЭД ни из удалённого реестра, ни из локального кэша.
Пожалуйста, попробуйте повторить свой запрос чуть позже."""


@app.command('phone')
def main(phone: str = typer.Argument('+79000000000')):
    typer.echo(GREETINGS_TEMPLATE.format(phone=phone))

    okved_service = get_okved_service()

    normalized_phone, matching_okved_data, normalization_error = okved_service.get_okved(raw_phone_number=phone)
    resulting_message = form_resulting_message(normalized_phone, matching_okved_data, normalization_error)
    typer.echo(resulting_message)


def form_resulting_message(normalized_phone: str, matching_okved_data, normalization_error) -> str:
    if not normalized_phone:
        return PHONE_NORMALIZATION_ERROR_TMP.format(phone_err=normalization_error)

    if matching_okved_data is None:
        return OKVED_LOAD_FAILED_MSG

    matches_count = matching_okved_data['matches_count']

    if matching_okved_data['complete_match']:
        return COMPLETE_MATCH_MSG_TEMPLATE.format(
            code_len=matches_count,
            code=matching_okved_data['okved'],
            title=matching_okved_data['title'],
        )
    elif matches_count:
        return INCOMPLETE_MATCH_MSG_TEMPLATE.format(
            code_len=matches_count,
            code=matching_okved_data['okved'],
            title=matching_okved_data['title'],
        )

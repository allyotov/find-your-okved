import logging

import typer

from src.services.okved import OkvedService

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = typer.Typer()


@app.command('phone')
def main(phone: str = typer.Argument('+79000000000')):
    typer.echo('Вас приветствует утилита "Найди свой ОКВЭД по номеру телефона".')
    typer.echo('Вы передали номер телефона: {phone};'.format(phone=phone))

    okved_service = OkvedService()

    okved_number, normalization_error = okved_service.get_okved(raw_phone_number=phone)
    typer.echo('Ваш ОКВЭД: {okved};'.format(okved=okved_number))
    if not okved_number:
        typer.echo(
            'Произошла ошибка нормализации телефонного номера:\n {phone_err};'.format(phone_err=normalization_error)
        )

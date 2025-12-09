import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    logger.info('Утилита "Найди свой ОКВЭД по номеру телефона" запущена.')


if __name__ == "__main__":
    main()

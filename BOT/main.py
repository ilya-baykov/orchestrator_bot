from contextlib import asynccontextmanager
from logging import getLogger

from core.models.db_helper import db_helper

logger = getLogger()


@asynccontextmanager
async def lifespan(app):
    # Запуск программы
    logger.info("Бот запущен")
    yield
    # Завершение программы
    logger.info("Бот завершил свою работу")
    db_helper.dispose()


if __name__ == '__main__':
    logger.info("Приложение запущено")

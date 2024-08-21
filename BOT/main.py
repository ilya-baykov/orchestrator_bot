import asyncio
import platform
from aiogram import Bot
from app.bot_running import start_bot
from database.TelegramUser.crud import TelegramUserCRUD
from database.core import db
from logger_settings import setup_logger


async def main():
    # await db.reset_database()
    # await db.create_db()

    await start_bot()


if __name__ == '__main__':
    print("Бот запущен")
    logger = setup_logger()
    try:
        # Установите политику цикла событий для Windows
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        asyncio.run(main())
    except Exception as e:
        print(e)

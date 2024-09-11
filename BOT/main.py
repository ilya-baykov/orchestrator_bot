import asyncio
import platform

import urllib3

from app.bot_running import start_bot
from database.core import db
from logger_settings import setup_logger


async def main():
    # await db.reset_database()
    await db.create_db()
    await db.reflect_tables(schema='orchestrator')
    await start_bot()


if __name__ == '__main__':
    print("Бот запущен")
    logger = setup_logger()
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    try:
        # Установите политику цикла событий для Windows
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

        asyncio.run(main())
    except Exception as e:
        print(e)

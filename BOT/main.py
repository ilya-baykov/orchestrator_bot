import asyncio
from database.core import db
from database.CRUD.create import create_user


async def main():
    # Создаем базу данных и таблицы
    await db.create_db()

    # Теперь можно создать пользователя
    user = await create_user(username="ilya", email="ilya@baykov", full_name="Байков Илья Павлович")
    print(f"Создан пользователь: {user}")


if __name__ == '__main__':
    asyncio.run(main())

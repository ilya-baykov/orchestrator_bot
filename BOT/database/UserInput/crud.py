from typing import List

from sqlalchemy import select
from database.UserInput.model import UserInput  # Убедитесь, что импортируете правильную модель
from database.base_crud import BaseCRUD
from database.core import db


class UserInputCRUD(BaseCRUD):
    model = UserInput

    @classmethod
    async def find_by_process_name(cls, user_input_id: int) -> List[UserInput]:
        """Получить все записи с тем же именем процесса, что и у записи с заданным ID"""
        async with db.Session() as session:
            # Запрос для получения всех записей с тем же именем процесса
            query = (
                select(cls.model)
                .where(cls.model.process_name ==
                       select(cls.model.process_name)
                       .where(cls.model.id == user_input_id)
                       .scalar_subquery())
            )

            result = await session.execute(query)
            return result.scalars().all

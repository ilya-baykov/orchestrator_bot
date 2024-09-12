import logging
from typing import List

from sqlalchemy import select
from database.UserInput.model import UserInput  # Убедитесь, что импортируете правильную модель
from database.base_crud import BaseCRUD
from database.core import db

logger = logging.getLogger(__name__)


class UserInputCRUD(BaseCRUD):
    model = UserInput

    @classmethod
    async def find_process_stages(cls, id: int) -> List[UserInput]:
        """Получить все записи с тем же именем процесса, что и у записи с заданным ID"""
        async with db.Session() as session:
            # Запрос для получения всех записей с тем же именем процесса
            query = (
                select(cls.model)
                .where(cls.model.process_name ==
                       select(cls.model.process_name)
                       .where(cls.model.id == id)
                       .scalar_subquery())
            )

            result = await session.execute(query)
            stages = result.scalars().all()
            logger.info(f"Этапы по процессу id = {id}: {stages}")
            return stages

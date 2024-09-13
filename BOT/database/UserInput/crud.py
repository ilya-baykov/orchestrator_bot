import logging
from typing import List

from sqlalchemy import select

from database.FilterTable.model import FilterTable
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

    @classmethod
    async def find_all(cls, department_access: str, **filter_by):
        async with db.Session() as session:
            # Создаем запрос с использованием join и фильтрации
            query = (
                select(cls.model)
                .join(FilterTable)
                .filter(FilterTable.department_access == department_access)
                .filter_by(**filter_by)
                .execution_options(schema=cls.schema)
            )
            result = await session.execute(query)
            logger.info(f"{cls} find_all department_access={department_access}, filter_by={filter_by} : {result}")
            return result.scalars().all()

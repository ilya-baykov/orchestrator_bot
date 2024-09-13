from datetime import datetime
from typing import Optional

from sqlalchemy import and_, select, func

from database.OrchestratorJobs.model import OrchestratorJobs
from database.base_crud import BaseCRUD
from database.core import db


class OrchestratorJobsCRUD(BaseCRUD):
    model = OrchestratorJobs
    schema = 'orchestrator'

    @classmethod
    async def find_latest_by_process_version(cls, process_version_id: int, start_time: datetime, end_time: datetime) \
            -> Optional[OrchestratorJobs]:
        """
        Находит последний объект OrchestratorJobs по заданному идентификатору версии процесса
        и диапазону времени создания.

        :param process_version_id: Идентификатор версии процесса для фильтрации.
        :param start_time: Начальное время диапазона для фильтрации по полю created.
        :param end_time: Конечное время диапазона для фильтрации по полю created.
        :return: Последний объект OrchestratorJobs, соответствующий условиям, или None, если не найден.
        """
        async with db.Session() as session:
            query = (
                select(cls.model)
                .filter(
                    and_(
                        cls.model.process_version_id == process_version_id,
                        cls.model.created.between(start_time, end_time)
                    )
                )
                .order_by(cls.model.created.desc())  # Сортируем по полю created в порядке убывания
                .limit(1)
            )
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_count_machine(cls, process_version_id: int, start_time: datetime, end_time: datetime) -> Optional[
        int]:
        """
        Получение количества уникальных robot_id, занятых процессом в заданный период времени.

        :param process_version_id: ID версии процесса, для которого нужно получить количество уникальных robot_id.
        :param start_time: Начальное время диапазона для фильтрации задач (в формате 'YYYY-MM-DD HH:MM:SS').
        :param end_time: Конечное время диапазона для фильтрации задач (в формате 'YYYY-MM-DD HH:MM:SS').
        :return: Количество уникальных robot_id или None, если запрос не вернул результатов.
        """
        async with db.Session() as session:
            query = (
                select(func.count(func.distinct(cls.model.robot_id)).label('количество_уникальных_robot_id'))
                .where(
                    and_(
                        cls.model.process_version_id == process_version_id,
                        cls.model.started.between(start_time, end_time)
                    )
                )
                .execution_options(schema=cls.schema)
            )
            result = await session.execute(query)
            count = result.scalar()  # Получаем значение из результата
            return count

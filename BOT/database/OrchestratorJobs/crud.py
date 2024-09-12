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
    async def find_all(cls, limit=None, order_by=None, **filter_by):
        async with db.Session() as session:
            query = select(cls.model)

            # Применяем фильтры (если есть)
            if filter_by:
                filters = [getattr(cls.model, key) == value for key, value in filter_by.items()]
                query = query.where(*filters)

            # Применяем сортировку
            if order_by is not None:  # Проверяем, что order_by не None
                query = query.order_by(order_by)

            # Применяем лимит, если указан
            if limit is not None:  # Проверяем, что limit не None
                query = query.limit(limit)

            query = query.execution_options(schema=cls.schema)
            result = await session.execute(query)
            return result.scalars().all()
            # Получение последней задачи:
            # last_job = await OrchestratorJobsCRUD.find_all(
            #     limit=1,
            #     order_by=OrchestratorJobs.created.desc(),  # Сортировка по полю created в порядке убывания
            #     process_version_id=1048  # Фильтр по process_version_id
            # )

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

            # start_time_dt = datetime(2023, 12, 22, 20, 0, 0)  # 2023-12-22 20:00:00
            # end_time_dt = datetime(2023, 12, 22, 23, 0, 0)  # 2023-12-22 23:00:00
            #
            # # Вызов метода с готовыми объектами datetime
            # cnt = await OrchestratorJobsCRUD.get_count_machine(process_version_id=1048, start_time=start_time_dt,
            #                                                    end_time=end_time_dt)
            # print(cnt)

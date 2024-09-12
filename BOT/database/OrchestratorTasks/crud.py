from datetime import datetime

from database.OrchestratorTasks.model import OrchestratorTasks
from database.base_crud import BaseCRUD
from database.core import db
from sqlalchemy import and_, select


class OrchestratorTasksCRUD(BaseCRUD):
    model = OrchestratorTasks
    schema = 'orchestrator'

    @classmethod
    async def find_by_queue_id_and_created(cls,
                                           queue_id: int, start_time: datetime, end_time: datetime,
                                           limit: int = 10) -> list[OrchestratorTasks]:
        """
        Находит задачи в очереди по идентификатору очереди и диапазону времени создания.

        :param queue_id: Идентификатор очереди, по которому будет выполнен поиск.
        :param start_time: Начальное время для фильтрации по полю 'created'.
        :param end_time: Конечное время для фильтрации по полю 'created' в формате
        :param limit: Максимальное количество возвращаемых записей (по умолчанию 10).
        :return: Список объектов OrchestratorTasks, соответствующих критериям поиска.
        """
        async with db.Session() as session:
            query = (
                select(cls.model)
                .filter(
                    and_(
                        cls.model.queue_id == queue_id,
                        cls.model.created.between(start_time, end_time)
                    )
                )
                .limit(limit)
                .execution_options(schema=cls.schema)
            )
            result = await session.execute(query)
            return result.scalars().all()

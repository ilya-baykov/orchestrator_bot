import logging

from database.OrchestratorQueues.model import OrchestratorQueues
from database.OrchestratorTasks.model import OrchestratorTasks
from database.base_crud import BaseCRUD
from database.core import db
from sqlalchemy import select, and_

from datetime import datetime

logger = logging.getLogger(__name__)


class OrchestratorTasksCRUD(BaseCRUD):
    model = OrchestratorTasks
    schema = 'orchestrator'

    @classmethod
    async def find_tasks_by_queue_guid_and_created(cls, queue_guid: str, start_time: datetime, end_time: datetime,
                                                   limit: int = 10) -> list[OrchestratorTasks]:
        """
        Находит задачи в очереди по GUID очереди и диапазону времени создания.

        :param queue_guid: GUID очереди, по которому будет выполнен поиск.
        :param start_time: Начальное время для фильтрации по полю 'created'.
        :param end_time: Конечное время для фильтрации по полю 'created'.
        :param limit: Максимальное количество возвращаемых записей (по умолчанию 10).
        :return: Список объектов OrchestratorTasks, соответствующих критериям поиска.
        """
        async with db.Session() as session:
            query = (
                select(OrchestratorTasks)
                .join(OrchestratorQueues)
                .filter(
                    and_(
                        OrchestratorQueues.guid == queue_guid,
                        OrchestratorTasks.created.between(start_time, end_time)
                    )
                )
                .limit(limit)
                .execution_options(schema=cls.schema)
            )
            result = await session.execute(query)
            tasks = result.scalars().all()
            logger.info(f"В очереди {queue_guid} было получено {len(tasks)} задач в период {start_time} - {end_time} ")
            return tasks

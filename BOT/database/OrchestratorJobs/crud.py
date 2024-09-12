from sqlalchemy import and_, select

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

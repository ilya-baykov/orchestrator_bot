import logging

from sqlalchemy import select

from database.core import db

logger = logging.getLogger(__name__)


class BaseCRUD:
    model = None
    schema = 'public'

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with db.Session() as session:
            query = select(cls.model).filter_by(id=model_id).execution_options(schema=cls.schema)
            result = await session.execute(query)
            logger.info(f"{cls} find_by_id : {result}")
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with db.Session() as session:
            query = select(cls.model).filter_by(**filter_by).execution_options(schema=cls.schema)
            result = await session.execute(query)
            logger.info(f"{cls} find_one_or_none {filter_by} : {result}")
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with db.Session() as session:
            query = select(cls.model).filter_by(**filter_by).execution_options(schema=cls.schema)
            result = await session.execute(query)
            logger.info(f"{cls} find_all {filter_by} : {result}")
            return result.scalars().all()

    @classmethod
    async def create(cls, **kwargs):
        async with db.Session() as session:
            new_row = cls.model(**kwargs)
            session.add(new_row)
            await session.commit()
            await session.refresh(new_row)
            return new_row

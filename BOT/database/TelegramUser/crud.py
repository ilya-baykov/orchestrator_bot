import logging
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.TelegramUser.model import TelegramUser
from database.base_crud import BaseCRUD
from database.core import db

logger = logging.getLogger(__name__)


class TelegramUserCRUD(BaseCRUD):
    model = TelegramUser

    @classmethod
    async def get_department_by_telegram_id(cls, telegram_id: str) -> Optional[str]:
        """Получить отдел, к которому 'привязан' сотрудник """
        async with db.Session() as session:
            query = (
                select(cls.model)
                .options(selectinload(cls.model.access_list))
                .filter(cls.model.telegram_id == telegram_id)
            )
            result = await session.execute(query)
            telegram_user_instance = result.scalar_one_or_none()

            if telegram_user_instance and telegram_user_instance.access_list:
                return telegram_user_instance.access_list.department
            return None

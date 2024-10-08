import logging

from aiogram.filters import BaseFilter
from aiogram.types import Message

logger = logging.getLogger(__name__)


class IsTrueContact(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        try:
            return message.contact.user_id == message.from_user.id
        except Exception as e:
            logger.info(f"При попытке проверить принадлежность номера телефона - произошла ошибка:{e}")

import logging

from aiogram.filters import BaseFilter
from aiogram.types import Message

from database.TelegramUser.crud import TelegramUserCRUD

logger = logging.getLogger(__name__)


class RegisteredUser(BaseFilter):
    """Глобальный фильтр для проверки регистрации у пользователя"""

    # Задаем список команд, для которых требуется проверка регистрации
    COMMANDS_REQUIRING_REGISTRATION = ['/get_process_info']

    @classmethod
    async def __call__(cls, message: Message) -> bool:

        if message.text not in cls.COMMANDS_REQUIRING_REGISTRATION:
            return True  # Если команда не требует проверки, пропускаем фильтр

        access_employee = await TelegramUserCRUD.find_one_or_none(telegram_id=str(message.from_user.id))
        if access_employee:
            return True

        logger.info(
            f"Незарегистрированный пользователь с telegram_id = {message.from_user.id} пытался взаимодействовать с ботом ")
        return False

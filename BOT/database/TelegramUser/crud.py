from database.TelegramUser.model import TelegramUser
from database.base_crud import BaseCRUD


class TelegramUserCRUD(BaseCRUD):
    model = TelegramUser

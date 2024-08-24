from difflib import get_close_matches
from typing import List

from database.TelegramUser.crud import TelegramUserCRUD
from database.UserInput.crud import UserInputCRUD


class ProcessSearcher:

    @staticmethod
    async def find_processes(telegram_id: str) -> List:
        """
        Находит процессы для заданного Telegram ID.

        :param telegram_id: ID пользователя в Telegram.
        :return: Список процессов, доступных для данного пользователя.
        """
        department = await TelegramUserCRUD.get_department_by_telegram_id(telegram_id)
        processes = await UserInputCRUD.find_all(department_access=department)
        return processes

    @staticmethod
    def get_suitable_processes(processes: List, search_text: str) -> List:
        """
        Находит подходящие процессы по заданному тексту.

        :param processes: Список процессов.
        :param search_text: Текст для поиска.
        :return: Список подходящих процессов.
        """
        return [process for process in processes if process.process_name.upper() == search_text.upper()]

    @staticmethod
    def get_close_matches(processes: List, search_text: str) -> List[str]:
        """
        Находит близкие совпадения для заданного текста.

        :param processes: Список процессов.
        :param search_text: Текст для поиска.
        :return: Список близких совпадений.
        """
        all_names = {process.process_name.upper() for process in processes}
        return get_close_matches(search_text.upper(), all_names, n=10, cutoff=0.7)

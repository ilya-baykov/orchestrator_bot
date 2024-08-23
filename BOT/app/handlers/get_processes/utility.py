from difflib import get_close_matches
from typing import List

from app.support_objects import UserInputDb
from database.TelegramUser.crud import TelegramUserCRUD


class ProcessSearcher:
    processes_objects = None
    all_process_names = None

    def __init__(self, input_process: str):
        self.input_process = input_process
        self.input_prefix = input_process.upper().split("_")[0]

    @classmethod
    async def create(cls, input_process: str, telegram_id: str):
        instance = cls(input_process)
        department_access = await TelegramUserCRUD.get_department_by_telegram_id(telegram_id)
        instance.processes_objects = await UserInputDb.get_processes_objects(department_access=department_access)
        instance.all_process_names = await UserInputDb.get_all_process_names()
        return instance

    def get_processes_by_prefix(self):
        return [process.name.upper() for process in self.processes_objects if
                self.input_prefix == process.name.split("_")[0]]

    def get_similar(self):
        all_names = {prefix_name.split("_")[0] for prefix_name in self.all_process_names}  # Все имена процессов
        matches = get_close_matches(self.input_prefix, all_names, n=10, cutoff=0.8)  # Поиск наиболее похожих
        if matches:
            return [match.upper() for match in matches]
        return None

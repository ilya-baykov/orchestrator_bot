import json
import logging
from datetime import datetime, timedelta
from difflib import get_close_matches
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, ValidationError

from database.TelegramUser.crud import TelegramUserCRUD
from database.UserInput.crud import UserInputCRUD
from requests_objects.tasks_api import TasksApi

logger = logging.getLogger(__name__)


# Определяем модель для параметров
class Parameters(BaseModel):
    type: int
    text: Dict[str, str]


# Определяем основную модель для задачи
class TaskItem(BaseModel):
    id: str
    guid: str
    name: str
    description: Optional[str]
    status: str
    parameters: Optional[Parameters]
    created: str
    updated: str
    postponed: Optional[str]
    priority: str
    deadline: Optional[str]
    comment: Optional[str]
    tags: Optional[str]
    retries: Optional[str]


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


class TaskService:
    def __init__(self, tasks_api: TasksApi, period: str):
        """
        :param tasks_api: Объект класса для формирования запроса к Оркестратору для получения информации по задачам
        :param period: Интересующий пользователя период (фильтрация по времени)
        """
        self.tasks_api = tasks_api
        self.period = period

    def _unix_time(self) -> str:
        """Формирует время в формате unix со смещением на нужный период"""
        if self.period == "За текущий час":
            return str((datetime.now() - timedelta(hours=1)).timestamp())
        elif self.period == "За текущий день":
            return str((datetime.now() - timedelta(days=1)).timestamp())
        elif self.period == "За текущий год":
            return str((datetime.now() - timedelta(days=365)).timestamp())
        else:
            raise Exception

    def get_tasks(self, queue_guid: str, status: int) -> List[TaskItem]:
        """
        Получает список отфильтрованных по времени и статусу задач из Оркестратора
        :param queue_guid: Гуид Очереди
        :param status: Интересующий статус процессов
        :return: Список задач в формате TaskItem
        """
        unix_time = self._unix_time()
        raw_tasks = self.tasks_api.get_filter_list_request(guid_queue=queue_guid,
                                                           filters={"status": status, "createdLater": unix_time})
        tasks = []
        for row in raw_tasks:
            if isinstance(row['parameters'], str):
                row['parameters'] = json.loads(row['parameters'])
            try:
                tasks.append(TaskItem(**row))  # Создаем экземпляр TaskItem
            except ValidationError as e:
                logger.error(f"Ошибка валидации : {row}, {e}")
        return tasks


class TaskReport:
    """Класс для формирования отчётного сообщения пользователю"""

    def __init__(self, in_progress_tasks: List[TaskItem], success_tasks: List[TaskItem],
                 application_failed_tasks: List[TaskItem],
                 business_failed_tasks: List[TaskItem]):
        self.in_progress_tasks = in_progress_tasks
        self.success_tasks = success_tasks
        self.application_failed_tasks = application_failed_tasks
        self.business_failed_tasks = business_failed_tasks

    @staticmethod
    def _generate_task_section(title: str, tasks: List[TaskItem], status: str) -> str:
        """Формирует строку в сообщения для конкретного статуса процесса"""
        if not tasks:
            return ""

        section = f"\n{title}:\n"
        for task in tasks:
            if isinstance(task, TaskItem):
                section += (f"ID: {task.id}, Имя: {task.name},\n"
                            f"Время создания: {task.created},\n"
                            f"Статус: {status}\n\n")
            else:
                section += f"Ошибка: Неверный тип данных для задачи: {task}\n"
        return section

    def generate_report(self) -> str:
        """Формирует общий отчёт по этапу процесса"""
        report = f"Количество задач в процессе выполнения: {len(self.in_progress_tasks)}\n"
        report += f"Количество успешных задач: {len(self.success_tasks)}\n"
        report += f"Количество задач с ошибками приложения: {len(self.application_failed_tasks)}\n"
        report += f"Количество задач с ошибками бизнеса: {len(self.business_failed_tasks)}\n\n"

        report += self._generate_task_section("Задачи в процессе", self.in_progress_tasks, "В процессе")
        report += self._generate_task_section("Задачи с ошибками приложения", self.application_failed_tasks,
                                              "Не выполнено (Ошибка приложения)")
        report += self._generate_task_section("Задачи с ошибками бизнеса", self.business_failed_tasks,
                                              "Не выполнено (Ошибка бизнеса)")

        return report

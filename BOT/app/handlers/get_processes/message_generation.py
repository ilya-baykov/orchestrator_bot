import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional
from app.handlers.get_processes.keyboard import CurrentPeriodOptions
from database.OrchestratorJobs.crud import OrchestratorJobsCRUD
from database.OrchestratorProcesses.crud import OrchestratorProcessesCRUD
from database.OrchestratorQueues.crud import OrchestratorQueuesCRUD
from database.OrchestratorTasks.crud import OrchestratorTasksCRUD
from database.OrchestratorTasks.model import OrchestratorTasks
from database.UserInput.model import UserInput

logger = logging.getLogger(__name__)


@dataclass
class OrchestratorFields:
    stage: UserInput  # Текущий этап
    job_status: str  # Статус последней работы
    count_machine: int  # Количество машин, занятых этапом
    tasks: List[OrchestratorTasks]  # Список транзакций по этапу


class TimeRangeCreator:
    """Класс определяющий временной диапазон для фильтрации"""

    def __init__(self, filtering_period: CurrentPeriodOptions | str):

        self.filtering_period = CurrentPeriodOptions.__members__.get(str(filtering_period))
        if not self.filtering_period:
            raise ValueError(
                f"Неверный период фильтрации, один из вариантов {list(CurrentPeriodOptions.__members__.keys())}")

        self._end_time, self._start_time = self._create_time_range()

    def _create_time_range(self) -> tuple[datetime, datetime]:
        """По периоду фильтрации устанавливает временный диапазон """
        end_time = datetime.now()
        if self.filtering_period == CurrentPeriodOptions.HOUR:  # Фильтрация за последний час
            return end_time - timedelta(hours=1), end_time
        elif self.filtering_period == CurrentPeriodOptions.DAY:  # Фильтрация за последний день
            return end_time - timedelta(days=1), end_time

    def get_time_range(self) -> tuple[datetime, datetime]:
        return self._end_time, self._start_time

    def time_range_user_text(self) -> str:
        return f"Временный диапазон: c {str(self._end_time)} до {str(self._start_time)}"


class TransactionCollector:
    """Класс для сбора информации по этапам """

    def __init__(self, stages: List[UserInput], filtering_period: CurrentPeriodOptions):
        """
        :param stages: Все этапы по полученному процессу
        :param filtering_period: Период для фильтрации
        """
        self.stages = stages
        self.start_time, self.end_time = TimeRangeCreator(filtering_period).get_time_range()

    async def _bypassing_stages(self) -> List[OrchestratorFields]:
        """Обходит все этапы и собирает общую информацию по всему процессу"""
        stages_info = []
        for stage in self.stages:
            stages_fields = await self._get_information_stage(stage)
            if stages_fields:
                stages_info.append(stages_fields)
                logger.info(f"По этапу {stage.subprocess_name} были сформирован: {stages_fields}")
            else:
                logger.info(f"По этапу {stage.subprocess_name} нет актуальных задач")
        return stages_info

    async def _get_information_stage(self, stage: UserInput) -> Optional[OrchestratorFields]:
        process = await OrchestratorProcessesCRUD.find_one_or_none(guid=stage.subprocess_guid)  # Получаем процесс
        process_version_id = process.process_version_id  # Получаем версию процесса

        job = await OrchestratorJobsCRUD.find_latest_by_process_version(process_version_id=process_version_id,
                                                                        start_time=self.start_time,
                                                                        end_time=self.end_time)
        if job:
            count_machine = await OrchestratorJobsCRUD.get_count_machine(process_version_id=process_version_id,
                                                                         start_time=self.start_time,
                                                                         end_time=self.end_time)

            queue = await OrchestratorQueuesCRUD.find_one_or_none(guid="58f47683-9b3e-43ad-8157-0507fa3fde47")

            tasks = await OrchestratorTasksCRUD.find_by_queue_id_and_created(queue_id=queue.id,
                                                                             start_time=self.start_time,
                                                                             end_time=self.end_time)

            stages_fields = OrchestratorFields(stage=stage, job_status=job.status, count_machine=count_machine,
                                               tasks=tasks)
            return stages_fields
        return None

    async def get_stages_info(self) -> List[OrchestratorFields]:
        """Возвращает сформированный список с информацией по этапам процесса"""
        return await self._bypassing_stages()


class MessageCreator:
    """Класс для формирования ответа пользователю на команду /get_process_info """

    def __init__(self, process_name: str, stages_info: List[OrchestratorFields]):
        """
        :param process_name: название процесса
        :param stages_info: Сформированный список с информацией по этапам процесса
        """
        self.process_name = process_name
        self.stages_info = stages_info
        self._answer_text = self._create_answer_text()

    def _create_answer_text(self):

        text = f"{self.process_name}\n"
        if self.stages_info:
            text += f"Процесс выполняется на {5} машинах\n\n"
            for cnt, stage in enumerate(iterable=self.stages_info, start=1):
                text += (f'{cnt}) {stage.stage.subprocess_name}'
                         f'Выполняется: {13}/{30};\n'
                         f'Успешно выполнено: {13}/{30};\n'
                         f'Бизнес ошибка: {13}/{30};\n'
                         f'Ошибка обработки: {13}/{30};\n'
                         f'Примерное время ожидания: {17} минут\n\n')
            text = f"Процесс еще будет выполняться ~ {34} минуты"
        else:
            text += f"За этот период процесс не был запущен"
        return text

    @property
    def answer_text(self):
        return self._answer_text

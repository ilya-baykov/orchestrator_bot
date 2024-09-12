# 1) Получить все этапы по процессу (поиск по id) - входной аргумент state_data.get('all_process_stages', [])
# 2) Получаем process_version_id (поиск по гуид этапа)
# 3) Получаем статус по последней работе (поиск по process_version_id и временному диапазону)
# 4) Получаем очередь (поиск по гуиду очереди)
# 5) Получаем задачи (поиск по id очереди)
from dataclasses import dataclass
from datetime import datetime
from typing import List

from database.OrchestratorJobs.crud import OrchestratorJobsCRUD
from database.OrchestratorJobs.model import OrchestratorJobs
from database.OrchestratorProcesses.crud import OrchestratorProcessesCRUD
from database.OrchestratorProcesses.model import OrchestratorProcesses
from database.OrchestratorQueues.crud import OrchestratorQueuesCRUD
from database.OrchestratorQueues.model import OrchestratorQueues
from database.OrchestratorTasks.crud import OrchestratorTasksCRUD
from database.OrchestratorTasks.model import OrchestratorTasks
from database.UserInput.model import UserInput


# * Из этапа процесса получаем :

# text = ('RPA012: Выплаты\n'
#         'Процесс выполняется на 6 машинах\n'
#         'На этапе "Формирование банковский и почтовых файлов": 13 транзакций\n'
#         'На этапе "Отправка СнО на согласование": 31 транзакций\n'
#         'Всего в обработке:46 транзакций\n'
#         'Упали в ошибку: 2 транзакции\n\n'
#         'Примерное время ожидания: 1 час 57 минут')
#
# await callback.message.edit_text(text=text)

class AnswerCreator:
    """Класс для формирования ответа пользователю на команду /get_process_info """

    def __init__(self, stages: List[UserInput]):
        """
        :param stages: Все этапы по полученному процессу
        """
        self.stages = stages
        self.start_time = datetime(2023, 12, 15, 14, 36, 13)
        self.end_time = datetime(2023, 12, 15, 14, 36, 13)

    @dataclass
    class OrchestratorFields:
        process_version_id: int
        job: OrchestratorJobs
        queue: OrchestratorQueues
        tasks: List[OrchestratorTasks]

    async def generation_information_stage(self, stage: UserInput):
        process = await OrchestratorProcessesCRUD.find_one_or_none(guid=stage.subprocess_guid)  # Получаем процесс
        process_version_id = process.process_version_id  # Получаем версию процесса

        job = await OrchestratorJobsCRUD.find_latest_by_process_version(
            process_version_id=process_version_id,
            start_time=self.start_time,
            end_time=self.end_time)

        count_machine = OrchestratorJobsCRUD.get_count_machine(process_version_id=process_version_id,
                                                               start_time=self.start_time,
                                                               end_time=self.end_time)

        queue = await OrchestratorQueuesCRUD.find_one_or_none(guid="58f47683-9b3e-43ad-8157-0507fa3fde47")

        tasks = await OrchestratorTasksCRUD.find_by_queue_id_and_created(queue_id=queue.id,
                                                                         start_time=self.start_time,
                                                                         end_time=self.end_time)
        print("Процесс", process)
        print("Версия процесса", process_version_id)
        print("Работа", job)
        print("Статус работы", job.status)
        print("Количество машин", count_machine)
        print("Задачи", tasks)

    def create_message_text(self):
        pass

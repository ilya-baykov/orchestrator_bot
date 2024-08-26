import json
import logging
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.handlers.get_processes.keyboard import create_inline_kb, ProcessInfo
from app.handlers.get_processes.state import OrchestratorProcessState
from app.handlers.get_processes.utility import ProcessSearcher, TaskItem
from global_filter import RegisteredUser
from requests_objects.tasks_api import tasks_api

logger = logging.getLogger(__name__)

orchestrator_process = Router()


@orchestrator_process.message(RegisteredUser(), Command('get_process_info'))
async def select_processor(message: Message, state: FSMContext):
    await state.set_state(OrchestratorProcessState.input_process_prefix)
    await message.answer("Введите название процесса, по которому хотите получить информацию")


@orchestrator_process.message(OrchestratorProcessState.input_process_prefix)
async def search_process(message: Message, state: FSMContext):
    """Обрабатывает сообщение и ищет процессы по префиксу."""

    try:
        processes = await ProcessSearcher.find_processes(str(message.from_user.id))  # Объект для поиска процессов
        suitable_processes = ProcessSearcher.get_suitable_processes(processes, message.text)  # Подходящие процессы

        if suitable_processes:
            await message.answer(text="Выберите нужный этап", reply_markup=await create_inline_kb(suitable_processes))
            await state.set_state(OrchestratorProcessState.input_current_process)
        else:
            matches = ProcessSearcher.get_close_matches(processes, message.text)  # Похожие по префиксу названия
            if matches:
                await message.answer(f"Возможно вы имели в виду: {str(matches)}")
            else:
                await message.answer("Такой процесс не найден")
    except Exception as e:
        await message.answer("Произошла ошибка при поиске процессов.")
        logger.error(f"При попытке найти нужные процессы по префиксу произошла ошибка: {e}")


@orchestrator_process.callback_query(ProcessInfo.filter())
async def choose_process(callback_query: CallbackQuery, callback_data: ProcessInfo, state: FSMContext):
    print(callback_data)
    await callback_query.answer(str(callback_data))
    try:
        success_tasks = tasks_api.get_filter_list_request(guid_queue=callback_data.queue_guid, filters={"status": 2})
        application_failed_tasks = tasks_api.get_filter_list_request(guid_queue=callback_data.queue_guid,
                                                                     filters={"status": 3})
        business_failed_tasks = tasks_api.get_filter_list_request(guid_queue=callback_data.queue_guid,
                                                                  filters={"status": 4})
        print(len(success_tasks))
        # Проходим по каждому элементу в списке
        for row in success_tasks:

            if isinstance(row['parameters'], str):  # Декодируем параметры, если они в виде строки
                row['parameters'] = json.loads(row['parameters'])

            # Создаем экземпляр модели
            task_item = TaskItem(**row)

            print(f"ID: {task_item.id}, Имя: {task_item.name}, Время создания: {task_item.created}")
        await callback_query.message.answer("Успешно")
    except Exception as e:
        logger.error(f"При попытке получить информацию из очереди произошла ошибка: {e}")
        await callback_query.message.answer("Произошла неизвестная ошибка")


def register_orchestrator_process_handlers(dp):
    dp.include_router(orchestrator_process)

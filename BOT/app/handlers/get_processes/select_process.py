import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.handlers.get_processes.keyboard import create_inline_kb, ProcessInfo, period_selection_kb
from app.handlers.get_processes.state import OrchestratorProcessState
from app.handlers.get_processes.utility import ProcessSearcher, TaskItem, TaskReport, TaskService
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


@orchestrator_process.message(OrchestratorProcessState.input_current_process,
                              F.text.in_({"За текущий час", "За текущий день", "За текущий год"}))
async def get_report_message(message: Message, state: FSMContext):
    state_data = await state.get_data()
    callback_data = state_data.get("callback_data")
    try:
        task_service = TaskService(tasks_api)  # Инициализируем TaskService
        success_tasks = task_service.get_tasks(callback_data.queue_guid, status=2)  # Получаем задачи
        application_failed_tasks = task_service.get_tasks(callback_data.queue_guid, status=3)  # Получаем задачи
        business_failed_tasks = task_service.get_tasks(callback_data.queue_guid, status=4)  # Получаем задачи
        in_progress_tasks = task_service.get_tasks(callback_data.queue_guid, status=1)  # Получаем задачи

        # Генерируем отчет
        task_report = TaskReport(in_progress_tasks, success_tasks, application_failed_tasks, business_failed_tasks)
        report_message = task_report.generate_report()
        await message.answer(report_message)
    except Exception as e:
        logger.error(f"При попытке получить информацию из очереди произошла ошибка: {e}")
        await message.answer("Произошла неизвестная ошибка")


@orchestrator_process.callback_query(ProcessInfo.filter())
async def choose_process(callback_query: CallbackQuery, callback_data: ProcessInfo, state: FSMContext):
    await callback_query.message.answer("Выберите нужный период", reply_markup=period_selection_kb)
    await state.update_data({"callback_data": callback_data})
    await callback_query.answer(str(callback_data))


def register_orchestrator_process_handlers(dp):
    dp.include_router(orchestrator_process)

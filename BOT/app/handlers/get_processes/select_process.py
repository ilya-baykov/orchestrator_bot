import logging
from datetime import datetime, timedelta
from typing import Union

from aiogram import Router, F, types
from aiogram.filters import Command, Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.handlers.get_processes.filter import LevelFilter
from app.handlers.get_processes.keyboard import stage_selection_kb, ProcessInfo, select_stage_mod_kb, \
    select_processes_kb, DisplayOptions, select_period_kb
from app.handlers.get_processes.state import OrchestratorProcessState
from global_filter import RegisteredUser
from requests_objects.tasks_api import tasks_api

logger = logging.getLogger(__name__)

orchestrator_process = Router()


#
# @orchestrator_process.message(RegisteredUser(), Command('get_process_info'))
# async def select_processor(message: Message, state: FSMContext):
#     await state.set_state(OrchestratorProcessState.input_process_prefix)
#     await message.answer("Введите название процесса, по которому хотите получить информацию")
#
#
# @orchestrator_process.message(OrchestratorProcessState.input_process_prefix)
# async def search_process(message: Message, state: FSMContext):
#     """Обрабатывает сообщение и ищет процессы по префиксу."""
#
#     try:
#         processes = await ProcessSearcher.find_processes(str(message.from_user.id))  # Объект для поиска процессов
#         suitable_processes = ProcessSearcher.get_suitable_processes(processes, message.text)  # Подходящие процессы
#
#         if suitable_processes:
#             await message.answer(text="Хотите посмотреть все этапы или какой-то конкретный ?", reply_markup=await display_mode_selection_keyboard())
#             await state.set_state(OrchestratorProcessState.input_current_process)
#             await state.update_data({"suitable_processes": suitable_processes})
#         else:
#             matches = ProcessSearcher.get_close_matches(processes, message.text)  # Похожие по префиксу названия
#             if matches:
#                 await message.answer(f"Возможно вы имели в виду: {str(matches)}")
#             else:
#                 await message.answer("Такой процесс не найден")
#     except Exception as e:
#         await message.answer("Произошла ошибка при поиске процессов.")
#         logger.error(f"При попытке найти нужные процессы по префиксу произошла ошибка: {e}")
#
#
# @orchestrator_process.message(OrchestratorProcessState.input_current_process,
#                               F.text.in_({"За текущий час", "За текущий день", "За текущий год"}))
# async def get_report_message(message: Message, state: FSMContext):
#     state_data = await state.get_data()
#     callback_data = state_data.get("callback_data")
#
#     try:
#         task_service = TaskService(tasks_api, period=message.text)  # Инициализируем TaskService
#         success_tasks = task_service.get_tasks(callback_data.queue_guid, status=2)
#         application_failed_tasks = task_service.get_tasks(callback_data.queue_guid, status=3)
#         business_failed_tasks = task_service.get_tasks(callback_data.queue_guid, status=4)
#         in_progress_tasks = task_service.get_tasks(callback_data.queue_guid, status=1)
#
#         # Генерируем отчет
#         task_report = TaskReport(in_progress_tasks, success_tasks, application_failed_tasks, business_failed_tasks)
#         report_message = task_report.generate_report()
#         await message.answer(report_message)
#     except Exception as e:
#         logger.error(f"При попытке получить информацию из очереди произошла ошибка: {e}")
#         await message.answer("Произошла неизвестная ошибка")
#
#
# @orchestrator_process.callback_query(F.data.in_(['all_stages', 'specific_stage']))
# async def handle_stage_selection(callback_query: CallbackQuery, state: FSMContext):
#     await callback_query.answer()  # Подтверждаем нажатие кнопки
#     state_data: dict = await state.get_data()
#     suitable_processes = state_data.get("suitable_processes", [])
#     if callback_query.data == 'all_stages':
#         await callback_query.message.answer("Вы выбрали все этапы.")
#         # Здесь можно добавить логику для обработки выбора "Все этапы"
#     elif callback_query.data == 'specific_stage':
#         await callback_query.message.answer("Выберите интересующий вас этап",
#                                             reply_markup=await stage_selection_kb(
#                                                 suitable_processes=suitable_processes))
#
#
# @orchestrator_process.callback_query(ProcessInfo.filter())
# async def choose_process(callback_query: CallbackQuery, callback_data: ProcessInfo, state: FSMContext):
#     await callback_query.message.answer("Выберите нужный период", reply_markup=period_selection_kb)
#     await state.update_data({"callback_data": callback_data})
#     await callback_query.answer(str(callback_data))


@orchestrator_process.message(Command('get_process_info'))
@orchestrator_process.callback_query(LevelFilter(level=1))
async def handle_process_info(message_or_callback: Union[types.Message, types.CallbackQuery]):
    """Отображает меню выбора нужного процесса и инициализирует уровень 1"""
    text, reply_markup = await select_processes_kb(level=1, telegram_id=str(message_or_callback.from_user.id))
    if isinstance(message_or_callback, types.Message):
        await message_or_callback.answer(text=text, reply_markup=reply_markup)
    else:
        await message_or_callback.message.edit_text(text=text, reply_markup=reply_markup)


@orchestrator_process.callback_query(LevelFilter(level=2))
async def handle_level_2(callback: types.CallbackQuery, state: FSMContext):
    """На этом этапе мы получаем id процесса формируем клавиатуру с выбором периода для фильтрации"""
    callback_data = ProcessInfo.unpack(callback.data)
    if callback_data.id:
        await state.update_data(id=callback_data.id)
    text, reply_markup = select_period_kb(level=callback_data.lvl, sizes=(3,))
    await callback.message.edit_text(text=text, reply_markup=reply_markup)


@orchestrator_process.callback_query(LevelFilter(level=3))
async def handle_level_3(callback: types.CallbackQuery, state: FSMContext):
    """На этом этапе мы получаем период фильтрации и формируем клавиатуру для ввода режима отображения статистики"""
    callback_data = ProcessInfo.unpack(callback.data)
    if callback_data.period:
        await state.update_data(period=callback_data.period)

    text, reply_markup = select_stage_mod_kb(level=callback_data.lvl)
    await callback.message.edit_text(text=text, reply_markup=reply_markup)


@orchestrator_process.callback_query(LevelFilter(level=4))
async def handle_level_4(callback: types.CallbackQuery, state: FSMContext):
    """На этом этапе мы получаем режим отображения статистики и при необходимости формируем клавиатуру с этапами"""
    callback_data = ProcessInfo.unpack(callback.data)
    if callback_data.mod:
        await state.update_data(mod=callback_data.mod)
    if callback_data.mod == DisplayOptions.ALL_STAGES.name:
        state_data = await state.get_data()
        await callback.message.edit_text(text=str(state_data))
    else:
        state_data = await state.get_data()
        text, reply_markup = await stage_selection_kb(level=callback_data.lvl, process_id=state_data.get('id', 0))
        await callback.message.edit_text(text=text, reply_markup=reply_markup)


@orchestrator_process.callback_query(LevelFilter(level=5))
async def handle_level_5(callback: types.CallbackQuery, state: FSMContext):
    callback_data = ProcessInfo.unpack(callback.data)  # Извлекаем данные из callback
    if callback_data.stage:
        await state.update_data(stage=callback_data.stage)
    state_data = await state.get_data()
    await callback.message.edit_text(text=str(state_data))


def register_orchestrator_process_handlers(dp):
    dp.include_router(orchestrator_process)

import logging
from typing import Union

from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.handlers.get_processes.filter import LevelFilter
from app.handlers.get_processes.keyboard import *
from app.handlers.get_processes.message_generation import MessageCreator, TransactionCollector
from app.handlers.get_processes.state import update_process_stages_if_not_exists, update_period_if_not_exists
from database.TelegramUser.crud import TelegramUserCRUD
from database.UserInput.crud import UserInputCRUD

logger = logging.getLogger(__name__)

orchestrator_process = Router()


@orchestrator_process.message(Command('get_process_info'))
@orchestrator_process.callback_query(LevelFilter(level=1))
async def handle_process_info(message_or_callback: Union[types.Message, types.CallbackQuery], state: FSMContext):
    """Отображает меню выбора нужного процесса и инициализирует уровень 1"""
    await state.update_data(all_process_stages=None)
    await state.update_data(period_options=None)

    # Получаем процессы, которые относятся к пользователю
    department = await TelegramUserCRUD.get_department_by_telegram_id(telegram_id=str(message_or_callback.from_user.id))
    processes = await UserInputCRUD.find_all(department_access=department)
    text, reply_markup = await select_processes_kb(level=1, processes=processes)
    if isinstance(message_or_callback, types.Message):
        await message_or_callback.answer(text=text, reply_markup=reply_markup)
    else:
        await message_or_callback.message.edit_text(text=text, reply_markup=reply_markup)


@orchestrator_process.callback_query(LevelFilter(level=2))
async def handle_level_2(callback: types.CallbackQuery, state: FSMContext):
    """На этом этапе мы получаем id процесса формируем клавиатуру с выбором периода для фильтрации"""
    callback_data = ProcessInfo.unpack(callback.data)
    if callback_data.id: await state.update_data(id=callback_data.id)  # Фиксируем id выбранного процесса
    await update_period_if_not_exists(state)  # Обновляем варианты периода фильтрации один раз для процесса
    state_data = await state.get_data()  # Получаем данные текущего состояния state
    text, reply_markup = select_period_kb(level=callback_data.lvl, sizes=(2,),
                                          ru_periods=state_data.get('period_options').split(';'))
    await callback.message.edit_text(text=text, reply_markup=reply_markup)


@orchestrator_process.callback_query(LevelFilter(level=3))
async def handle_level_3(callback: types.CallbackQuery, state: FSMContext):
    """На этом этапе мы получаем период фильтрации и формируем клавиатуру для ввода режима отображения статистики"""
    callback_data = ProcessInfo.unpack(callback.data)
    if callback_data.period: await state.update_data(period=callback_data.period)  # Фиксируем период для фильтрации
    text, reply_markup = select_stage_mod_kb(level=callback_data.lvl)
    await callback.message.edit_text(text=text, reply_markup=reply_markup)


@orchestrator_process.callback_query(LevelFilter(level=4))
async def handle_level_4(callback: types.CallbackQuery, state: FSMContext):
    """На этом этапе мы получаем режим отображения статистики и при необходимости формируем клавиатуру с этапами"""
    callback_data = ProcessInfo.unpack(callback.data)
    if callback_data.mod: await state.update_data(mod=callback_data.mod)  # Фиксируем режим отображения

    await update_process_stages_if_not_exists(state=state)  # Подгружаем один раз все этапы
    state_data = await state.get_data()  # Получаем всю нужную информацию для формирования запроса
    all_process_stages = state_data.get('all_process_stages', [])  # Информация по всем выбранным этапам
    period = state_data.get('period')  # Информация по периоду фильтрации
    if callback_data.mod == DisplayOptions.ALL_STAGES.name:  # Если выбрали 'Показать все этапы'
        stages_info = await TransactionCollector(stages=all_process_stages, filtering_period=period).get_stages_info()
        answer: str = MessageCreator(stages_info=stages_info).answer_text
        await callback.message.edit_text(text=answer)
    else:
        text, reply_markup = await stage_selection_kb(level=callback_data.lvl,
                                                      suitable_processes=all_process_stages)
        await callback.message.edit_text(text=text, reply_markup=reply_markup)


@orchestrator_process.callback_query(LevelFilter(level=5))
async def handle_level_5(callback: types.CallbackQuery, state: FSMContext):
    callback_data = ProcessInfo.unpack(callback.data)  # Извлекаем данные из callback
    if callback_data.stage: await state.update_data(stage_id=callback_data.stage)  # Фиксируем выбранный этап

    state_data = await state.get_data()  # Получаем всю нужную информацию для формирования запроса
    period = state_data.get('period')  # Информация по периоду фильтрации
    stage_id = state_data.get('stage_id')  # id выбранного этапа
    all_process_stages = state_data.get('all_process_stages', [])  # Все возможные этапы для выбранного процесса

    # Получение нужного этапа
    selected_stage = next((stage for stage in all_process_stages if stage.id == stage_id), None)
    stage_info = await TransactionCollector(stages=[selected_stage], filtering_period=period).get_stages_info()
    answer: str = MessageCreator(stages_info=stage_info).answer_text
    await callback.message.edit_text(text=answer)


def register_orchestrator_process_handlers(dp):
    dp.include_router(orchestrator_process)

from dataclasses import dataclass
from typing import Optional, Dict, Any

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.UserInput.crud import UserInputCRUD


class OrchestratorProcessState(StatesGroup):
    input_process_prefix = State()
    input_current_process = State()


async def update_process_stages_if_not_exists(state: FSMContext):
    """
    Обновляет информацию по всем этапам, если она еще не была загружена.
    Метод был создан для избежания лишнего использования 'ресурсоёмкий' операций с UserInputCRUD

    :param state: Контекст состояния.
    """
    state_data = await state.get_data()

    if not state_data.get('all_process_stages', None):
        process_id = state_data.get('id', 0)  # Получаем id из состояния
        all_process_stages = await UserInputCRUD.find_process_stages(id=process_id)
        await state.update_data(all_process_stages=all_process_stages)
        return all_process_stages

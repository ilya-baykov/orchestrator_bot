import logging

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.FilterTable.crud import FilterTableCRUD
from database.FilterTable.model import FilterTable
from database.UserInput.crud import UserInputCRUD
from exeptions import NoProcessById

logger = logging.getLogger(__name__)


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


async def update_period_if_not_exists(state: FSMContext) -> None:
    """
    Обновляет информацию по вариантам фильтрации периодов транзакций.
    Теперь варианты периодов фильтрации(Час, День, Месяц... задаются в таблице FilterTable ) для каждого процесса
    Метод был создан для избежания лишнего использования 'ресурсоёмкий' операций с FilterTableCRUD

    :param state: Контекст состояния.
    """
    state_data = await state.get_data()

    if not state_data.get('period_options', None):
        process_id = state_data.get('id', 0)  # Получаем id из состояния
        all_period_options: FilterTable = await FilterTableCRUD.find_one_or_none(fk_id=process_id)
        if all_period_options:
            logger.info(
                f"Для процесса id = {process_id} были получены такие варианты фильтрации:{all_period_options}")
            await state.update_data(period_options=all_period_options.filtration_period)
        else:
            raise NoProcessById(f"Не получилось найти процесс по id = {process_id}")

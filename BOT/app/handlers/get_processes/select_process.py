import logging
from difflib import get_close_matches

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.handlers.get_processes.state import OrchestratorProcessState
from app.handlers.get_processes.utility import ProcessSearcher
from database.TelegramUser.crud import TelegramUserCRUD
from database.UserInput.crud import UserInputCRUD
# from app.handlers.get_processes.utility import ProcessSearcher
from global_filter import RegisteredUser

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
            await message.answer(str(suitable_processes))
        else:
            matches = ProcessSearcher.get_close_matches(processes, message.text)  # Похожие по префиксу названия
            if matches:
                await message.answer(f"Возможно вы имели в виду: {str(matches)}")
            else:
                await message.answer("Такой процесс не найден")
    except Exception as e:
        await message.answer("Произошла ошибка при поиске процессов.")
        logger.error(f"При попытке найти нужные процессы по префиксу произошла ошибка: {e}")


def register_orchestrator_process_handlers(dp):
    dp.include_router(orchestrator_process)

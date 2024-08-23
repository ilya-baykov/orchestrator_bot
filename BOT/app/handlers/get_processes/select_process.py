import logging

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.handlers.get_processes.state import OrchestratorProcessState
from app.handlers.get_processes.utility import ProcessSearcher
from global_filter import RegisteredUser

logger = logging.getLogger(__name__)

orchestrator_process = Router()


@orchestrator_process.message(RegisteredUser(), Command('get_process_info'))
async def select_processor(message: Message, state: FSMContext):
    await state.set_state(OrchestratorProcessState.input_process_prefix)
    await message.answer("Введите название процесса, по которому хотите получить информацию")


@orchestrator_process.message(OrchestratorProcessState.input_process_prefix)
async def search_process(message: Message, state: FSMContext):
    try:

        process_searcher = await ProcessSearcher.create(input_process=message.text,
                                                        telegram_id=str(message.from_user.id))
        processes_names = process_searcher.get_processes_by_prefix()  # Получаем имена процессов по префиксу

        if processes_names:  # Если такой префикс найден среди процессов - возвращаем имена процессов с таким же префиксом
            await message.answer(str(processes_names))
            await state.set_state(OrchestratorProcessState.input_current_process)
        else:
            matches = process_searcher.get_similar()  # Поиск похожих процессов
            if matches:
                await message.answer(f"Возможно, вы имели в виду: {str(matches)}")
            else:
                await message.answer("Такие процессы не найдены.")

    except Exception as e:
        await message.answer("Произошла ошибка при поиске процессов.")
        logger.error(f"При попытке найти нужные процессы по префиксу произошла ошибка: {e}")


def register_orchestrator_process_handlers(dp):
    dp.include_router(orchestrator_process)

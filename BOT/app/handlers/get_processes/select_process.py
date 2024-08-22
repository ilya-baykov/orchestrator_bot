import logging
from dataclasses import dataclass
from difflib import get_close_matches
from typing import List, Dict

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.handlers.get_processes.state import OrchestratorProcessState
from app.support_objects import OrchestratorProcessBD, OrchestratorProcess
from database.OrchestratorProcess.crud import OrchestratorProcessCRUD
from requests_objects.process_api import process_api

logger = logging.getLogger(__name__)

orchestrator_process = Router()


@orchestrator_process.message(Command('get_process_info'))
async def select_processor(message: Message, state: FSMContext):
    await state.set_state(OrchestratorProcessState.input_process)
    await message.answer("Введите название процесса, по которому хотите получить информацию")


@orchestrator_process.message(OrchestratorProcessState.input_process)
async def search_process(message: Message, state: FSMContext):
    try:
        # Получаем объекты процессов из базы данных
        processes_objects: List[OrchestratorProcess] = await OrchestratorProcessBD.get_processes_objects()
        input_process_prefix = message.text.lower().split("_")[0]  # Извлекаем префикс введённого процесса

        # Подходящие по префиксу имена процессов
        processes_names = [processes.name.upper() for processes in processes_objects if
                           input_process_prefix == processes.name.split("_")[0]]

        if processes_names:
            await message.answer(str(processes_names))
        else:
            all_names = {prefix_name.split("_")[0] for prefix_name in
                         await OrchestratorProcessBD.get_all_process_names()}  # Все имена процессов
            matches = get_close_matches(input_process_prefix, all_names, n=10, cutoff=0.8)  # Поиск наиболее похожих
            if matches:
                matches = '\n'.join(match.upper() for match in matches)
                await message.answer(f"Возможно, вы имели в виду:\n{matches}")
            else:
                await message.answer("Такие процессы не найдены.")

    except Exception as e:
        await message.answer("Произошла ошибка при поиске процессов.")
        logger.error(f"При попытке найти нужные процессы по префиксу произошла ошибка: {e}")


def register_orchestrator_process_handlers(dp):
    dp.include_router(orchestrator_process)

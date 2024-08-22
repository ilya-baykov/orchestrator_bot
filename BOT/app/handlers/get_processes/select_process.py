from difflib import get_close_matches

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.handlers.get_processes.state import OrchestratorProcess
from requests_objects.process_api import process_api

orchestrator_process = Router()


@orchestrator_process.message(Command('get_process_info'))
async def select_processor(message: Message, state: FSMContext):
    await state.set_state(OrchestratorProcess.input_process)
    await message.answer("Введите название процесса, по которому хотите получить информацию")


@orchestrator_process.message(OrchestratorProcess.input_process)
async def search_process(message: Message, state: FSMContext):
    # all_processes = tasks_api.get_filter_list_request(guid_queue=None)
    # matches = get_close_matches(message.text, all_processes, n=5, cutoff=0.3)
    # if matches:
    #     exact_matches = get_close_matches(message.text, all_processes, n=1, cutoff=0.95)  # Совпадение более 90%
    #     if exact_matches:
    #         await state.update_data({"exact_matches": exact_matches[0]})
    #         await message.answer(exact_matches[0])
    #     else:
    #         matches = ', '.join(matches)  # Совпадения более 30%
    #         await state.update_data({"matches": matches})
    #         await message.answer(matches)
    #     await message.answer("Похожие процессы не найдены")
    process = process_api.get_requests(message.text.lower())
    if process:
        await message.answer("Процесс Найден !")

    else:
        await message.answer("Процесс не Найден !")
    await message.answer(str(process))


def register_orchestrator_process_handlers(dp):
    dp.include_router(orchestrator_process)

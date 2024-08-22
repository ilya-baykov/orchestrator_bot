from aiogram.fsm.state import State, StatesGroup


class OrchestratorProcess(StatesGroup):
    input_process = State()

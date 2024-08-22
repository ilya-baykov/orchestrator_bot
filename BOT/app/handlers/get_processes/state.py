from aiogram.fsm.state import State, StatesGroup


class OrchestratorProcessState(StatesGroup):
    input_process = State()

from aiogram.fsm.state import State, StatesGroup


class OrchestratorProcessState(StatesGroup):
    input_process_prefix = State()
    input_current_process = State()

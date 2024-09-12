from database.OrchestratorTasks.model import OrchestratorTasks
from database.base_crud import BaseCRUD


class OrchestratorTasksCRUD(BaseCRUD):
    model = OrchestratorTasks
    schema = 'orchestrator'

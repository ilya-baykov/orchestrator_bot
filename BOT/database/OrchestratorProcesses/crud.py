from database.OrchestratorProcesses.model import OrchestratorProcesses
from database.base_crud import BaseCRUD



class OrchestratorProcessesCRUD(BaseCRUD):
    model = OrchestratorProcesses
    schema = 'orchestrator'

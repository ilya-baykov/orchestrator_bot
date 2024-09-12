from database.OrchestratorQueues.model import OrchestratorQueues
from database.base_crud import BaseCRUD
from database.core import db


class OrchestratorQueuesCRUD(BaseCRUD):
    model = OrchestratorQueues
    schema = 'orchestrator'

from select import select

from database.OrchestratorJobs.model import OrchestratorJobs
from database.base_crud import BaseCRUD
from database.core import db


class OrchestratorJobsCRUD(BaseCRUD):
    model = OrchestratorJobs
    schema = 'orchestrator'

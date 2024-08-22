from dataclasses import dataclass
from typing import List

from database.OrchestratorProcess.crud import OrchestratorProcessCRUD


@dataclass
class OrchestratorProcess:
    name: str
    guid: str


class OrchestratorProcessBD:
    __processes_objects: List[OrchestratorProcess] = None

    @classmethod
    async def get_processes_objects(cls) -> List[OrchestratorProcess]:
        if cls.__processes_objects is None:
            processes = await OrchestratorProcessCRUD.find_all()
            cls.__processes_objects = [OrchestratorProcess(name=process.process_name, guid=process.process_guid) for
                                       process in processes]
        return cls.__processes_objects

    @classmethod
    async def get_all_process_names(cls) -> List[str]:
        processes_objects = await cls.get_processes_objects()
        return [process.name for process in processes_objects]

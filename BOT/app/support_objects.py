from dataclasses import dataclass
from typing import List

from database.UserInput.crud import UserInputCRUD


@dataclass
class UserInputData:
    name: str
    guid: str


class UserInputDb:
    __processes_objects: List[UserInputData] = None

    @classmethod
    async def get_processes_objects(cls, **fileter) -> List[UserInputData]:
        if cls.__processes_objects is None:
            processes = await UserInputCRUD.find_all(**fileter)
            cls.__processes_objects = [UserInputData(name=process.subprocess_name, guid=process.subprocess_guid) for
                                       process in processes]
        return cls.__processes_objects

    @classmethod
    async def get_all_process_names(cls) -> List[str]:
        processes_objects = await cls.get_processes_objects()
        return [process.name for process in processes_objects]

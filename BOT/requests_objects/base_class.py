from abc import ABC, abstractmethod
from typing import Dict, Any


class GetRequests(ABC):
    def __init__(self, _api_client) -> None:
        """
        Инициализация API для работы с процессами.

        :param _api_client: Экземпляр клиента API. :ApiClient
        """
        self.api_client = _api_client

    @abstractmethod
    def get_requests(self, guid: str) -> Dict[str, Any]:
        pass

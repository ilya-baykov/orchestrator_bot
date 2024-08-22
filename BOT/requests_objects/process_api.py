from typing import Dict, Any, Optional

from requests_objects import api_client
from requests_objects.base_class import GetRequests


class ProcessApi(GetRequests):

    def get_requests(self, guid: str) -> Optional[Dict[str, Any]]:
        """
        Получение данных о процессе по его GUID.

        :param guid: Уникальный идентификатор процесса.
        :return: Данные о процессе в формате JSON.
        """
        endpoint = f"/api/process/read/{guid}"
        try:
            return self.api_client.get(endpoint)
        except Exception as e:
            print(e)
            return None


process_api = ProcessApi(api_client)


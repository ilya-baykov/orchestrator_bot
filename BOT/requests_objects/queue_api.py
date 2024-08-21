from typing import Dict, Any, Optional

from objects_requests.base_class import GetRequests


class QueuesApi(GetRequests):

    def get_requests(self, guid: str) -> Optional[Dict[str, Any]]:
        """
        Получение данных об очереди по его GUID.

        :param guid: Уникальный идентификатор очереди.
        :return: Данные о процессе в формате JSON.
        """
        endpoint = f"/api/queue/read/{guid}"
        try:
            return self.api_client.get(endpoint)
        except Exception as e:
            print(e)
            return None

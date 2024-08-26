import json
from typing import Dict, Any, Optional
from requests_objects.api_client import api_client

from requests_objects.base_class import GetRequests


class TasksApi(GetRequests):

    def get_requests(self, guid: str) -> Optional[Dict[str, Any]]:
        """
        Получение данных о задаче по его GUID.

        :param guid: Уникальный идентификатор очереди.
        :return: Данные о задаче в формате JSON.
        """
        endpoint = f"/api/task/read/{guid}"
        try:
            return self.api_client.get(endpoint)
        except Exception as e:
            print(e)
            return None

    def get_filter_request(self, guid_queue: str, filters: Optional[dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        """
        Получение данных о задачах с применением фильтров.

        :param guid_queue: Уникальный идентификатор очереди.
        :param filters: Словарь с фильтрами для запроса.
        :return: Данные о задачах в формате JSON.
        """
        if filters:
            filters = ";".join(f"{key}={value}" for key, value in filters.items())  # Формируем фильтры для запроса
            endpoint = f"/api/task/filter/read/{guid_queue}/{filters}"
        else:
            endpoint = f"/api/task/filter/read/{guid_queue}"
        try:
            return self.api_client.get(endpoint)
        except Exception as e:
            print(e)
            return None

    def get_filter_list_request(self, guid_queue: str,
                                filters: Optional[dict[str, str]] = None) -> Optional[Dict[str, Any]]:

        """
        Получение данных о нескольких задачах с применением фильтров.

        :param guid_queue: Уникальный идентификатор очереди.
        :param filters: Словарь с фильтрами для запроса.
        :return: Данные о задачах в формате JSON.
        """
        if filters:
            filters = ";".join(f"{key}={value}" for key, value in filters.items())  # Формируем фильтры для запроса

            endpoint = f"/api/task/filter/list/{guid_queue}/{filters}"
        else:
            endpoint = f"/api/task/filter/list/{guid_queue}"
        try:
            return self.api_client.get(endpoint)
        except Exception as e:
            print(e)
            return None


tasks_api = TasksApi(api_client)

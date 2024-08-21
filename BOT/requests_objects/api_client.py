import os
from typing import Optional, Dict, Any

import requests


class ApiClient:
    def __init__(self, base_url: str) -> None:
        """
        Инициализация клиента API.

        :param base_url: Базовый URL для API.
        """
        self.base_url = base_url
        self.headers = {
            "Authorization": os.getenv("Authorization"),
            "Content-Type": "application/json"
        }

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Выполнение GET-запроса к API.

        :param endpoint: Конечная точка API.
        :param params: Параметры запроса.
        :return: Ответ API в формате JSON.
        """
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params, verify=False)
        self._handle_response(response)
        return response.json()

    @staticmethod
    def _handle_response(response: requests.Response) -> None:
        """
        Обработка ответа API.

        :param response: Ответ API.
        :raises Exception: Если статус-код ответа не 200.
        """
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code}, {response.text}")

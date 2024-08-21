from logging import getLogger, basicConfig, DEBUG, FileHandler, StreamHandler, Formatter
from datetime import datetime
import os

LOG_FORMAT = '%(asctime)s : %(name)s : %(levelname)s : %(message)s'
LOGS_DIR = os.getenv("LOGS_PATH", "define me!")  # получаем путь к папке LOGS
os.makedirs(LOGS_DIR, exist_ok=True)  # Проверка наличия папки (при ее отсутствии - создание)


def setup_logger():
    logger = getLogger()

    # Настройка файла логов
    log_file_path = os.path.join(LOGS_DIR, f"Logger_{datetime.today().strftime('%d_%m_%Y')}.log")
    file_handler = FileHandler(log_file_path, mode="a")
    file_handler.setLevel(DEBUG)

    # Настройка консольного вывода
    console_handler = StreamHandler()
    console_handler.setLevel(DEBUG)

    # Установка формата для обработчиков
    file_handler.setFormatter(Formatter(LOG_FORMAT))
    console_handler.setFormatter(Formatter(LOG_FORMAT))

    # Настройка базовой конфигурации логгирования
    basicConfig(level=DEBUG, handlers=[file_handler, console_handler])

    return logger

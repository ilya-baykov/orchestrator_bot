import enum
from abc import ABC, abstractmethod
from typing import List, Optional, Any, Tuple, Type
from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.TelegramUser.crud import TelegramUserCRUD
from database.UserInput.crud import UserInputCRUD
from database.UserInput.model import UserInput


#
# class ProcessInfo(CallbackData, prefix="process_info_kb"):
#     id: int
#     queue_guid: str
#
#
# async def stage_selection_kb(suitable_processes: List[UserInput]):
#     """
#
#     :param suitable_processes: Процессы, подходящие под запрос пользователя
#     :return: Объект inline-клавиатуры
#     """
#     keyboard = InlineKeyboardBuilder()
#     for process in suitable_processes:
#         callback_data = ProcessInfo(id=process.id, queue_guid=process.queue_guid)
#
#         keyboard.add(InlineKeyboardButton(text=f"{process.stage}",
#                                           callback_data=callback_data.pack()))
#
#     return keyboard.adjust(1).as_markup()
#
#
# async def display_mode_selection_keyboard():
#     # Создаем клавиатуру для предоставления выбора нужного этапа процесса / всех этапов
#     button_all_stages = types.InlineKeyboardButton(text="Все этапы", callback_data="all_stages")
#     button_specific_stage = types.InlineKeyboardButton(text="Конкретный этап", callback_data="specific_stage")
#
#     # Создаем клавиатуру с кнопками
#     keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
#         [button_all_stages],  # Первая строка с кнопкой "Все этапы"
#         [button_specific_stage]  # Вторая строка с кнопкой "Конкретный этап"
#     ])
#
#     return keyboard
#
#
# period_selection_kb = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text="За текущий час"),
#             KeyboardButton(text="За текущий день"),
#             KeyboardButton(text="За текущий год"),
#         ]
#
#     ],
#     resize_keyboard=False,
#     one_time_keyboard=True,
#     input_field_placeholder="Выберите интересующий вас период"
# )
class DisplayOptions(enum.Enum):
    ALL_STAGES = "Все этапы"
    SPECIFIC_STAGE = "Конкретный этап"


class ProcessInfo(CallbackData, prefix="processes_menu"):
    level: Optional[int] = None
    process_name: Optional[str] = None
    stage_mod: Optional[str] = None
    stage: Optional[str] = None

    def __init__(self, level: int, process_name: Optional[str] = None, stage_mod: Optional[str] = None,
                 stage: Optional[str] = None):
        super().__init__()
        self.level = level
        self.process_name = process_name
        self.stage_mod = stage_mod
        self.stage = stage


#
class KeyboardsCreator(ABC):

    def __init__(self, buttons: dict[str, Any]):
        self.buttons = buttons
        self.keyboard = InlineKeyboardBuilder()

    @abstractmethod
    def create(self, sizes: tuple[int] = (2,)):
        pass


class ReplyKeyboardsCreator(KeyboardsCreator):
    def create(self, sizes: Tuple[int] = (2,), **kwargs):
        """
        Создает клавиатуру типа ReplyKeyboardMarkup на основе кнопок из словаря.

        :param:sizes : Tuple[int], optional Количество кнопок в каждой строке (по умолчанию (2,)).
        **kwargs : keyword arguments (resize_keyboard,one_time_keyboard,input_field_placeholder)
        """
        keyboard_buttons = [
            [KeyboardButton(text=text) for text in list(self.buttons.keys())[i:i + sizes[0]]]
            for i in range(0, len(self.buttons), sizes[0])
        ]

        self.keyboard = ReplyKeyboardMarkup(
            keyboard=keyboard_buttons,
            resize_keyboard=kwargs.get('resize_keyboard', False),
            one_time_keyboard=kwargs.get('one_time_keyboard', True),
            input_field_placeholder=kwargs.get('input_field_placeholder', "Выберите интересующий вас период")
        )

        return self.keyboard


class InlineKeyboardsCreator(KeyboardsCreator):
    def create(self, sizes: tuple[int] = (2,)):
        for text, data in self.buttons.items():
            self.keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

        # Добавляем кнопку "Назад" внизу
        back_button = InlineKeyboardButton(
            text="Назад",
            callback_data=ProcessInfo(level=self.get_previous_level()).pack()
        )
        self.keyboard.add(back_button)

        return self.keyboard.adjust(*sizes).as_markup()

    def get_previous_level(self):
        # Метод для получения предыдущего уровня
        return self.buttons.get("level", 1) - 1  # Пример, как можно получить уровень


async def select_processes_kb(process_info: ProcessInfo, telegram_id: str, sizes: tuple[int] = (2,)):
    department = await TelegramUserCRUD.get_department_by_telegram_id(telegram_id)
    processes = await UserInputCRUD.find_all(department_access=department)

    # Увеличиваем уровень на 1 для следующего шага
    next_level = process_info.level + 1

    buttons = {}
    for process in processes:
        # Упаковываем данные для кнопки, используя следующий уровень
        buttons[str(process.process_name)] = ProcessInfo(
            process_name=process.process_name,
            level=next_level,  # Используем увеличенный уровень
            stage_mod=process_info.stage_mod  # Сохраняем stage_mod, если он есть
        ).pack()

    return "Выберите процесс:", InlineKeyboardsCreator(buttons=buttons).create(sizes=sizes)


def select_stage_mod_kb(process_info: ProcessInfo, sizes: tuple[int] = (2,),
                        display_options: Type[enum.Enum] = DisplayOptions):
    buttons = {
        option.value: ProcessInfo(level=int(process_info.level) + 1, stage_mod=option.name,
                                  process_name=process_info.process_name).pack()
        for option in display_options
    }
    return "Выберите режим отображения статистики:", InlineKeyboardsCreator(buttons=buttons).create(sizes=sizes)


async def stage_selection_kb(process_info: ProcessInfo, sizes: tuple[int] = (2,)):
    suitable_processes: List[UserInput] = await UserInputCRUD.find_all(process_name=process_info.process_name)

    buttons = {
        process.stage: ProcessInfo(level=int(process_info.level) + 1, process_name=process_info.process_name,
                                   stage=process.stage).pack()
        for process in suitable_processes
    }

    return "Выберите нужный этап:", InlineKeyboardsCreator(buttons=buttons).create(sizes=sizes)

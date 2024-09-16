import enum
from abc import ABC, abstractmethod
from typing import List, Optional, Any, Tuple, Type
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.UserInput.model import UserInput


class CurrentPeriodOptions(enum.Enum):
    """Перечисление для различных временных периодов с их русскими названиями."""

    HOUR = 'За последний час'
    DAY = 'За последний день'
    WEEKLY = 'За последнюю неделю'
    MONTH = 'За последний месяц'
    YEAR = 'За последний год'

    @classmethod
    def get_value_ru_key(cls, ru_key: str) -> Optional['CurrentPeriodOptions']:
        """
        Получает значение перечисления на основе ключа на русском языке.

        :param ru_key: Ключ на русском языке, который нужно найти в значениях перечисления.
        :return: Значение перечисления, соответствующее найденному ключу, или None, если ключ не найден.
        """
        for key, value in cls.__members__.items():
            # Проверяем, содержится ли ru_key в значении перечисления (без учета регистра)
            if ru_key.lower() in value.value.lower():
                return value
        return None


class DisplayOptions(enum.Enum):
    ALL_STAGES = "Все этапы"
    SPECIFIC_STAGE = "Конкретный этап"


class ProcessInfo(CallbackData, prefix="menu"):
    lvl: Optional[int] = None
    id: Optional[int] = None
    stage: Optional[int] = None
    mod: Optional[str] = None
    period: Optional[str] = None


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
    def create(self, sizes: tuple[int] = (2,), current_level: int = None):
        for text, data in self.buttons.items():
            self.keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

        # Добавляем кнопку "Назад", если текущий уровень задан
        if int(current_level) > 1:
            back_button = InlineKeyboardButton(
                text="Назад",
                callback_data=ProcessInfo(lvl=int(current_level) - 1).pack()
            )
            self.keyboard.add(back_button)

        return self.keyboard.adjust(*sizes).as_markup()


async def select_processes_kb(level: int, processes: List[UserInput], sizes: tuple[int] = (2,)):
    buttons = {str(process.process_name): ProcessInfo(id=process.id, lvl=level + 1).pack()
               for process in processes}
    return "Выберите процесс:", InlineKeyboardsCreator(buttons=buttons).create(sizes=sizes,
                                                                               current_level=level)


def select_stage_mod_kb(level, sizes: tuple[int] = (2,), display_options: Type[enum.Enum] = DisplayOptions):
    buttons = {
        option.value: ProcessInfo(lvl=level + 1, mod=option.name).pack()
        for option in display_options
    }
    return "Выберите режим отображения статистики:", InlineKeyboardsCreator(buttons=buttons).create(sizes=sizes,
                                                                                                    current_level=level)


async def stage_selection_kb(level: int, suitable_processes: List[UserInput], sizes: tuple[int] = (2,)):
    buttons = {
        process.stage: ProcessInfo(lvl=level + 1, stage=process.id).pack()
        for process in suitable_processes
    }

    return "Выберите нужный этап:", InlineKeyboardsCreator(buttons=buttons).create(sizes=sizes,
                                                                                   current_level=level)


def select_period_kb(level: int, ru_periods: list, sizes: tuple[int] = (2,)):
    buttons = {
        period.value: ProcessInfo(lvl=level + 1, period=period.name).pack()
        for ru_period in ru_periods
        if (period := CurrentPeriodOptions.get_value_ru_key(ru_period))
    }

    return "Выберите за какой период показать статистику:", InlineKeyboardsCreator(buttons=buttons).create(sizes=sizes,
                                                                                                           current_level=level)

from typing import List

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.UserInput.model import UserInput


class ProcessInfo(CallbackData, prefix="process_info_kb"):
    id: int
    queue_guid: str


async def create_inline_kb(suitable_processes: List[UserInput]):
    """

    :param suitable_processes: Процессы, подходящие под запрос пользователя
    :return: Объект inline-клавиатуры
    """
    keyboard = InlineKeyboardBuilder()
    for process in suitable_processes:
        callback_data = ProcessInfo(id=process.id, queue_guid=process.queue_guid)

        keyboard.add(InlineKeyboardButton(text=f"{process.stage}",
                                          callback_data=callback_data.pack()))

    return keyboard.adjust(1).as_markup()


period_selection_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="За текущий час"),
            KeyboardButton(text="За текущий день"),
            KeyboardButton(text="За текущий год"),
        ]

    ],
    resize_keyboard=False,
    one_time_keyboard=True,
    input_field_placeholder="Выберите интересующий вас период"
)

from aiogram import types
from aiogram.filters import Filter

from app.handlers.get_processes.keyboard import ProcessInfo


class LevelFilter(Filter):
    def __init__(self, level: int):
        self.level = level

    async def __call__(self, callback: types.CallbackQuery):
        callback_data = ProcessInfo.unpack(callback.data)
        return callback_data.lvl == self.level

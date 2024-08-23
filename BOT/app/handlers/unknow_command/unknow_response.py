from aiogram import Router, Dispatcher
from aiogram.types import Message

from global_filter import RegisteredUser
from throttling_middleware import ThrottlingMiddleware

unknown_command = Router()
unknown_command.message.middleware(ThrottlingMiddleware(limit=2))


@unknown_command.message(RegisteredUser())
async def unknown_response(message: Message):
    await message.answer("Неизвестная команда")


def register_unknown_command(dp: Dispatcher):
    dp.include_router(unknown_command)

import re
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from database.OrchestratorTasks.crud import OrchestratorTasksCRUD
from throttling_middleware import ThrottlingMiddleware
from app.handlers.start.filter import IsTrueContact
from app.handlers.start.keyboard import sent_contact_kb
from app.handlers.start.state import UserRegistration
from database.TelegramUser.crud import TelegramUserCRUD
from database.AccessList.crud import AccessListCRUD

start = Router()
start.message.middleware(ThrottlingMiddleware(limit=2))




@start.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    """Обработчик стартовой команды"""
    user = await TelegramUserCRUD.find_one_or_none(telegram_id=str(message.from_user.id))
    if user:
        await message.answer(f"{message.from_user.username}, вы уже были успешно зарегистрированы")
    else:
        await state.set_state(UserRegistration.input_phone)
        await message.answer(f"{message.from_user.username}, для продолжения необходимо зарегистрироваться\n"
                             f"Отправьте свой контактный номер, привязанный к этому аккаунту!",
                             reply_markup=sent_contact_kb)


@start.message(UserRegistration.input_phone, F.contact, IsTrueContact())
async def get_user_contact(message: Message, state: FSMContext):
    phone_number = re.sub(r'^\+?7', '8', message.contact.phone_number)
    access_employee = await AccessListCRUD.find_one_or_none(phone=str(phone_number))
    if access_employee:
        await TelegramUserCRUD.create(telegram_username=message.from_user.username,
                                      telegram_id=str(message.from_user.id), access_list_id=access_employee.id)
        await message.answer(f"{access_employee.fullname}, вы успешно зарегистрировались в этом чат-боте")
    else:
        await message.answer("Извините, для вас нет доступа к функционалу этого бота")
    await state.clear()


def register_start_handlers(dp):
    dp.include_router(start)

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    Message,
    InlineKeyboardMarkup, WebAppInfo,
)
from aiogram import Router, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from utils.quick_resto import get_bonus_info
from states.states import Register
from orm import BotUserManager

# from config import config
from keyboards.make_keyboards import make_row_keyboard, make_inline_keyboard, make_url_keyboard, make_contact_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    if await BotUserManager().get_by_telegram_id(telegram_id=message.from_user.id):
        cachback_info = await get_bonus_info(message.from_user.id)
        await message.answer(
        f"Здравствуйте, {html.quote(message.from_user.first_name)}."
        f"\nВаш уровень кешбека: {cachback_info}"
        # f"\nКоличество баллов: {}"
    )
    else:
        await message.answer(f"Здравствуйте, {html.quote(message.from_user.first_name)}!\n\nПоделитесь своим номером телефона,чтобы отслеживать свой статус системы лояльности. ",
                             reply_markup=make_contact_keyboard())
        await state.set_state(Register.phone)

@router.message(Command("help"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('Чтобы зайти в главное меню, нажмите /start\nЕсли у Вас есть какие-то вопросы, то пишите в поддержку - @support_borodino')

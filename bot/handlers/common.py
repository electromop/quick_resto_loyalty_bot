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
from aiogram.types import Message, ReplyKeyboardRemove

from utils.quick_resto import get_bonus_info
from states.states import Register
from orm import BotUserManager

from extensions import qri_sdk

# from config import config
from keyboards.make_keyboards import make_row_keyboard, make_inline_keyboard, make_url_keyboard, make_contact_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user = await BotUserManager().get_by_telegram_id(telegram_id=message.from_user.id)
    if user:
        cachback_info = await get_bonus_info(user.quick_resto_id)
        await message.answer(
        f"Здравствуйте, {html.quote(message.from_user.first_name)}."
        f"\n\nВаш уровень: {cachback_info['bonus_level']} - {cachback_info['bonus_percent']}%"
        f"\nКоличество баллов: {cachback_info['bonus_balance']}",
        reply_markup=make_inline_keyboard({'История списаний': 'bonus_history'}).as_markup()
        )
    else:
        await message.answer(f"Здравствуйте, {html.quote(message.from_user.first_name)}!\n\nПоделитесь своим номером телефона,чтобы отслеживать свой статус системы лояльности. ",
                             reply_markup=make_contact_keyboard())
        await state.set_state(Register.phone)

@router.callback_query(lambda call: call.data=="to_main")
async def cmd_start_callback(callback_data: Message, state: FSMContext):
    user = await BotUserManager().get_by_telegram_id(telegram_id=callback_data.from_user.id)
    if user:
        cachback_info = await get_bonus_info(user.quick_resto_id)
        await callback_data.message.answer(
        f"Здравствуйте, {html.quote(callback_data.from_user.first_name)}."
        f"\nВаш уровень кешбека: {cachback_info['bonus_level']} {cachback_info['bonus_percent']}"
        f"\nКоличество баллов: {cachback_info['bonus_balance']}",
         reply_markup=make_inline_keyboard({'История списаний': 'bonus_history'}).as_markup()
        )
    else:
        await callback_data.message.answer(f"Здравствуйте, {html.quote(callback_data.from_user.first_name)}!\n\nПоделитесь своим номером телефона,чтобы отслеживать свой статус системы лояльности. ",
                             reply_markup=make_contact_keyboard())
        await state.set_state(Register.phone)

@router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext):
    await message.answer('Введите:\n/start - чтобы зайти в главное меню\n\nЕсли у Вас есть какие-то вопросы, то пишите в поддержку - @support_borodino', reply_markup=ReplyKeyboardRemove())
    await state.clear()

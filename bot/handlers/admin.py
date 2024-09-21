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
from states.states import Campaign
from orm import BotUserManager

# from config import config
from keyboards.make_keyboards import make_row_keyboard, make_inline_keyboard, make_url_keyboard, make_contact_keyboard

router = Router()

@router.message(Command("admin"))
async def cmd_start(message: Message, state: FSMContext):
    user = await BotUserManager().get_by_telegram_id(telegram_id=message.from_user.id)
    if user.is_admin:
        await message.answer(
        f"Здравствуйте, {html.quote(message.from_user.first_name)}."
        f"Вы зашли в Админ панель бота",
        reply_markup=make_inline_keyboard({
            "Создать рассылку": "create_campaign"
        })
    )
    else:
        await message.answer(f"К сожалению, у Вас нет доступа к этой команде(\nЕсли что-то непонятно - введите /help.",
                             reply_markup=make_contact_keyboard())

@router.callback_query(lambda call: call.data=="create_campaign")
async def create_campaign(callback_data: Message, state: FSMContext):
    await callback_data.answer('Отправьте сообщение, которое хотите разослать всем пользователям:')
    await state.set_state(Campaign.campaign_text)

@router.message(StateFilter(Campaign.campaign_text))
async def create_campaign(message: Message, state: FSMContext):
    await message.answer(f"Начинаем отправку...")
    for user in await BotUserManager().get_all():
        await message.bot.send_message(chat_id=user.telegram_id, text=message.text)
    await message.answer(f"Сообщение отправлено всем пользователям")
    await state.clear()

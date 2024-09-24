import logging
import asyncio

from aiogram import Router, html, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types import (
    InlineKeyboardButton,
    Message,
    InlineKeyboardMarkup, WebAppInfo,
)

from utils.quick_resto import create_client, get_bonus_info, get_bonus_history
from states.states import Register
from config import Config

# from config import config
from keyboards.make_keyboards import *
from extensions import qri_sdk
from models import BotUser
from orm import BotUserManager
from datetime import datetime


router = Router()

@router.callback_query(lambda call: call.data=="bonus_history")
async def bonus_history(callback_data: Message, state: FSMContext):
    user = await BotUserManager().get_by_telegram_id(telegram_id=callback_data.from_user.id)
    if user:
        cachback_info = await get_bonus_history(user.quick_resto_id)
        print(cachback_info)
        await callback_data.message.answer(
            cachback_info,
            reply_markup=make_inline_keyboard({"Назад":'to_main'}).as_markup()
        )
    else:
        await callback_data.message.answer("Что-то пошло не так...")

# @router.callback_query(lambda call: call.data=="to_main")
# async def to_main(callback_data: Message, state: FSMContext):
#     if await BotUserManager().get_by_telegram_id(telegram_id=callback_data.from_user.id):
#         cachback_info = await get_bonus_info(callback_data.from_user.id)
#         await callback_data.answer(
#         f"Здравствуйте, {html.quote(callback_data.from_user.first_name)}."
#         f"\nВаш уровень кешбека: {cachback_info}"
#         # f"\nКоличество баллов: {}"
#     )

import logging
import asyncio

from aiogram import Router, html
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types import (
    InlineKeyboardButton,
    Message,
    InlineKeyboardMarkup, WebAppInfo,
)

from utils.quick_resto import client_exists, create_client, get_bonus_info
from states.states import Register
from config import Config

# from config import config
from keyboards.make_keyboards import *
from extensions import Session
from models import BotUser
from orm import BotUserManager
from datetime import datetime


router = Router()

@router.message(Command('register'))
async def cmd_register(message: Message, state: FSMContext):
    if await BotUserManager().get_by_telegram_id(telegram_id=message.from_user.id):
        kb = make_inline_keyboard({'Да': 'reauthorize_yes', 'Нет':'reauthorize_no'})
        await message.answer('Вы уже авторизованы!\nХотите зайти под другим номером телефона?', reply_markup=kb)
    else:
        await message.answer("Пожалуйста, поделитесь своим номером телефона, чтобы авторизироваться", reply_markup=make_contact_keyboard())
        await state.set_state(Register.phone)


@router.message(StateFilter(Register.phone))
async def cmd_register_phone(message: Message, state: FSMContext):
    await message.answer("Одну минуту, мы ищем Вас в нашей базе...")
    try:
        phone = message.contact.phone_number
        quick_resto_id = await client_exists(phone)

        if quick_resto_id:
            telegram_id = message.from_user.id

            user = BotUser(telegram_id=telegram_id,
                        quick_resto_id=quick_resto_id,
                        phone=phone,
                        creation_date=datetime.now().date())

            await BotUserManager().add(user)
            await message.answer("Вы успешно авторизировались!", reply_markup=ReplyKeyboardRemove())
            await state.clear()
            if await BotUserManager().get_by_telegram_id(telegram_id=message.from_user.id):
                cachback_info = await get_bonus_info(message.from_user.id)
                await message.answer(
                f"Здравствуйте, {html.quote(message.from_user.first_name)}."
                f"\nВаш уровень кешбека: {cachback_info}"
                # f"\nКоличество баллов: {}"
            )
            else:
                await message.answer('Ошибка авторизации. Попробуйте еще раз')
        else:
            await message.answer(
                "К сожалению, Вы еще не зарегистрированы в системе лояльности."
                "Хотите зарегистрироваться?",
                reply_markup=make_inline_keyboard({'Да': 'register_yes', 'Нет': 'register_no'})
                )
            state.update_data({'phone': phone})
    except Exception as e:
        print(e)
        await message.answer("Упс! Вы отправили что-то другое. Нажмите на кнопку ниже, чтобы авторизироваться", reply_markup=make_contact_keyboard())
        await state.clear()

@router.callback_query(lambda call: call.data=="reauthorize_yes")
async def reauthorize_yes(callback_data: Message, state: FSMContext):
    await callback_data.answer("Чтобы авторизироваться напишите свой номер телефона:")
    await state.set_state(Register.phone)


@router.callback_query(lambda call: call.data=="reauthorize_no")
async def reauthorize_no(callback_data: Message, state: FSMContext):
    await callback_data.answer('Хорошо.\nЕсли что-то непонятно введите /help')

@router.callback_query(lambda call: call.data=="register_yes")
async def register_yes(callback_data: Message, state: FSMContext):
    phone = state.get_data()['phone']
    quick_resto_id = await create_client(callback_data.from_user.full_name, phone)
    telegram_id = callback_data.message.from_user.id
    
    user = BotUser(telegram_id=telegram_id,
                        quick_resto_id=quick_resto_id,
                        phone=phone,
                        creation_date=datetime.now().date())

    await BotUserManager().add(user)
    await callback_data.answer("Спасибо! Теперь Вы зарегистрированы в системе лояльности.")
    if await BotUserManager().get_by_telegram_id(telegram_id=callback_data.from_user.id):
        cachback_info = await get_bonus_info(callback_data.from_user.id)
        await callback_data.answer(
            f"Здравствуйте, {html.quote(callback_data.from_user.first_name)}."
            f"\nВаш уровень кешбека: {cachback_info}"
            # f"\nКоличество баллов: {}"
        )
    else:
        await callback_data.answer('Ошибка авторизации. Попробуйте еще раз')

@router.callback_query(lambda call: call.data=="register_no")
async def register_no(callback_data: Message, state: FSMContext):
    await callback_data.answer('Хорошо.\nЕсли что-то непонятно введите /help')

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

from utils.quick_resto import create_client, get_bonus_info, search_client, get_client_info, add_start_group
from states.states import Register
from config import Config

from keyboards.make_keyboards import *
# from extensions import Session
from models import BotUser
from orm import BotUserManager
from datetime import datetime


router = Router()

@router.message(Command('register'))
async def cmd_register(message: Message, state: FSMContext):
    if await BotUserManager().get_by_telegram_id(telegram_id=message.from_user.id):
        kb = make_inline_keyboard({'Да': 'reauthorize_yes', 'Нет':'reauthorize_no'})
        await message.answer('Вы уже авторизованы!\n\nХотите зайти под другим номером телефона?', reply_markup=kb.as_markup())
    else:
        await message.answer("Пожалуйста, поделитесь своим номером телефона, чтобы авторизироваться", reply_markup=make_contact_keyboard())
        await state.set_state(Register.phone)

@router.message(StateFilter(Register.phone))
async def cmd_register_phone(message: Message, state: FSMContext):
    await message.answer(html.italic("Одну минуту, ищем Ваш номер среди клиентов..."), reply_markup=ReplyKeyboardRemove())
    # try:
    phone = message.contact.phone_number
    user_id = await search_client(phone)
    print(user_id)
    if user_id:
        user = await get_client_info(user_id)
        if not user.get("customerGroup"):
            await message.answer(
                    f"{html.italic('К сожалению, Вы еще не зарегистрированы в системе лояльности.')}"
                    "\n\nХотите зарегистрироваться?",
                    reply_markup=make_inline_keyboard({'Да': 'register_yes_update', 'Нет': 'register_no'}).as_markup()
                )
            await state.set_data({'user_id': user_id, "phone": phone, "telegram_id":message.from_user.id})
        elif user["customerGroup"]['name'] in ["СТАРТ", "2", "3", "4"]:
            telegram_id = message.from_user.id

            db_user = BotUser(telegram_id=telegram_id,
                            quick_resto_id=user["id"],
                            phone=phone,
                            creation_date=datetime.now().date())

            await BotUserManager().add(db_user)
            await message.answer("Вы успешно авторизировались!", reply_markup=ReplyKeyboardRemove())
            await state.clear()
            if await BotUserManager().get_by_telegram_id(telegram_id=message.from_user.id):
                cachback_info = await get_bonus_info(db_user.quick_resto_id)
                await message.answer(
                        f"Здравствуйте, {html.quote(message.from_user.first_name)}."
                        f"\n\nВаш уровень: {cachback_info['bonus_level']}"
                        f"\nПроцент кешбека: {int(cachback_info['bonus_percent'])}%"
                        f"\nКоличество баллов: {cachback_info['bonus_balance']}",
                        reply_markup=make_inline_keyboard({'История списаний': 'bonus_history'}).as_markup()
                        )
            else:
                    await message.answer('Ошибка авторизации. Попробуйте еще раз.')
        else:
                await message.answer(
                    f"{html.italic('К сожалению, Вы еще не зарегистрированы в системе лояльности.')}"
                    f"\n\nМы подарим приветственный бонус в размере {html.bold('200 баллов')}, если присоединитесь сейчас)"
                    "\n\nХотите зарегистрироваться?",
                    reply_markup=make_inline_keyboard({'Да': 'register_yes', 'Нет': 'register_no'}).as_markup()
                )
    else:
        await message.answer(
                f"{html.italic('К сожалению, Вы еще не зарегистрированы в системе лояльности.')}"
                f"\n\nМы подарим приветственный бонус в размере {html.bold('200 баллов')}, если присоединитесь сейчас)"
                "\n\nХотите зарегистрироваться?",
                reply_markup=make_inline_keyboard({'Да': 'register_yes', 'Нет': 'register_no'}).as_markup()
                )
        await state.update_data({'phone': phone})
    # except Exception as e:
    #     print(e)
    #     await message.answer("Упс! Вы отправили что-то другое. Нажмите на кнопку ниже, чтобы авторизироваться", reply_markup=make_contact_keyboard())
    #     await state.clear()

@router.callback_query(lambda call: call.data=="reauthorize_yes")
async def reauthorize_yes(callback_data: Message, state: FSMContext):
    await callback_data.message.answer("Чтобы авторизироваться, напишите свой номер телефона:", reply_markup=make_contact_keyboard())
    await state.set_state(Register.phone)


@router.callback_query(lambda call: call.data=="reauthorize_no")
async def reauthorize_no(callback_data: Message, state: FSMContext):
    await callback_data.message.answer('Хорошо.\nЕсли что-то непонятно введите /help', reply_markup=ReplyKeyboardRemove())


@router.callback_query(lambda call: call.data=="register_yes")
async def register_yes(callback_data: Message, state: FSMContext):
    await callback_data.message.answer(html.italic("Пожалуйста, введите свое ФИО, чтобы мы знали как к Вам обращаться:"))
    await state.set_state(Register.phone_after_name)

@router.callback_query(lambda call: call.data=="register_yes_update")
async def register_yes_update(callback_data: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    response = await add_start_group(user_id)
    db_user = BotUser(telegram_id=data.get("telegram_id"),
                            quick_resto_id=user_id,
                            phone=data.get("phone"),
                            creation_date=datetime.now().date())

    await BotUserManager().add(db_user)
    await callback_data.message.answer("Вы успешно зарегистрированы в системе лояльности! Чтобы продолжить нажмите /start")
    await state.clear()

@router.message(StateFilter(Register.phone_after_name))
async def cmd_register_name(message: Message, state: FSMContext):
    await message.answer(html.italic("Одну минуту, создаем Ваш профиль..."))
    phone_data = await state.get_data()
    phone = phone_data['phone']
    user_id= await search_client(phone)
    first_name = message.text.split(' ')[0]
    last_name = message.text.split(' ')[1]
    middle_name = message.text.split(' ')[2]
    if not user_id:
        new_user = await create_client(first_name, last_name, phone)
        telegram_id = message.from_user.id
            
        db_user = BotUser(telegram_id=telegram_id,
                        quick_resto_id=new_user['id'],
                        phone=phone,
                        creation_date=datetime.now().date())

        await BotUserManager().add(db_user)
        await message.answer("Спасибо! Теперь Вы зарегистрированы в системе лояльности.\n\nЧтобы зайти в главное меню нажмите /start")
        await state.clear()
        if await BotUserManager().get_by_telegram_id(telegram_id=message.from_user.id):
            cachback_info = await get_bonus_info(user_id)
            await message.answer(
                    f"Здравствуйте, {html.quote(message.from_user.first_name)}."
                    f"\n\nВаш уровень: {cachback_info['bonus_level']}"
                    f"\nПроцент кешбека: {int(cachback_info['bonus_percent'])}%"
                    f"\nКоличество баллов: {cachback_info['bonus_balance']}",
                    reply_markup=make_inline_keyboard({"История списаний": 'bonus_history'}).as_markup()
            )
        else:
            await message.answer('Ошибка регистрация. Попробуйте еще раз или напишите менеджеру @поддержка')
    else:
        db_user = BotUser(telegram_id=telegram_id,
                        quick_resto_id=user_id,
                        phone=phone,
                        creation_date=datetime.now().date())

        await BotUserManager().add(db_user)

        await message.answer(html.bold("Спасибо! Теперь Вы зарегистрированы в системе лояльности."))

        if await BotUserManager().get_by_telegram_id(telegram_id=message.from_user.id):
            cachback_info = await get_bonus_info(user_id)
            await message.answer(
                    f"Здравствуйте, {html.quote(message.from_user.first_name)}."
                    f"\n\nВаш уровень: {cachback_info['bonus_level']}"
                    f"\nПроцент кешбека: {int(cachback_info['bonus_percent'])}%"
                    f"\nКоличество баллов: {cachback_info['bonus_balance']}",
                    reply_markup=make_inline_keyboard({"История списаний": "bonus_history"}).as_markup()
            )
        else:
            await message.answer('Ошибка регистрация. Попробуйте еще раз или напишите менеджеру @поддержка')

@router.callback_query(lambda call: call.data=="register_no")
async def register_no(callback_data: Message, state: FSMContext):
    await callback_data.message.answer('Хорошо.\nЕсли что-то непонятно, введите /help', reply_markup=ReplyKeyboardRemove())

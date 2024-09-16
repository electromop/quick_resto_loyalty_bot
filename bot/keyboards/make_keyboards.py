from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def make_inline_keyboard(items: dict[str], prefix: str = "") -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for k, v in items.items():
        builder.add(InlineKeyboardButton(text=k, callback_data=f"{prefix}{v}"))
    return builder


def make_url_keyboard(items: dict[str]) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for k, v in items.items():
        builder.add(InlineKeyboardButton(text=k, url=f"{v}"))
    return builder


def make_contact_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отправить номер телефона 📱", request_contact=True)]],
                                   resize_keyboard=True)
    return keyboard


def make_geo_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отправить геолокацию", request_location=True)]],
                                   resize_keyboard=True)
    return keyboard

# К каждому уведомлению данного раздела прикрепляются кнопки “Подтвердить запись” и “Отменить запись”. В зависимости от ответа пользователя в СРМ системе изменяется статус записи пользователя с "ожидание" на "клиент подтвердил" или "Клиент не пришел".

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks import AttendanceCallback, ReviewCallback

def attendance_keyboard(record_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text="Подтвердить запись", callback_data=AttendanceCallback.new(record_id=record_id, action="confirm"))
    builder.button(text="Отменить запись", callback_data=AttendanceCallback.new(record_id=record_id, action="cancel"))
    
    return builder.as_markup()
    
def review_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text="Поставить оценку", callback_data=ReviewCallback.new(mark="rate"))

    return builder.as_markup()

def marks_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for i in range(1, 6):
        builder.button(text=str(i), callback_data=ReviewCallback.new(mark=str(i)))
    
    return builder.as_markup()

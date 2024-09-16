# К каждому уведомлению данного раздела прикрепляются кнопки “Подтвердить запись” и “Отменить запись”. В зависимости от ответа пользователя в СРМ системе изменяется статус записи пользователя с "ожидание" на "клиент подтвердил" или "Клиент не пришел".

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks import AttendanceCallback, ReviewCallback

def attendance_keyboard(record_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text="Подтвердить запись", callback_data=AttendanceCallback(record_id=record_id, action="confirm"))
    builder.button(text="Отменить запись", callback_data=AttendanceCallback(record_id=record_id, action="cancel"))
    
    return builder.as_markup()
    
def review_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    builder.button(text="Поставить оценку", callback_data=ReviewCallback(mark="rate", text=''))

    return builder.as_markup()

def marks_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for i in range(1, 6):
        builder.button(text=str(i), callback_data=ReviewCallback(mark=str(i), text=""))
    
    return builder.as_markup()
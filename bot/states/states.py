from aiogram.fsm.state import State, StatesGroup

class Register(StatesGroup):
    name = State()
    city = State()
    phone = State()

class Review(StatesGroup):
    text_review = State()


    
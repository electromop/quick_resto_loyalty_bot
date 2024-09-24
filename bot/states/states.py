from aiogram.fsm.state import State, StatesGroup

class Register(StatesGroup):
    name = State()
    city = State()
    phone = State()
    phone_after_name = State()

class Review(StatesGroup):
    text_review = State()

class Campaign(StatesGroup):
    campaign_text = State()


    
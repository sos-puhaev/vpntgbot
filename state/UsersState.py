from aiogram.dispatcher.filters.state import StatesGroup, State

class UsersState(StatesGroup):
    user = State()
    protocol = State()
    country = State()
    price = State()
    pay = State()

    
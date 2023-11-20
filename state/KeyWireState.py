from aiogram.dispatcher.filters.state import StatesGroup, State

class KeyWireState(StatesGroup):
    message_one = State()
    message_two = State()
    message_three = State()
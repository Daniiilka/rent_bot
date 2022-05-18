from aiogram.dispatcher.filters.state import StatesGroup, State


class UserInfo(StatesGroup):
    waiting_for_init = State()
    waiting_for_start = State()
    waiting_for_type = State()
    waiting_for_district = State()
    waiting_for_period = State()
    waiting_for_price = State()
    waiting_for_rooms = State()
    waiting_for_condition = State()
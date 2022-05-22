from aiogram.dispatcher.filters.state import State, StatesGroup


class UserInfo(StatesGroup):
    waiting_for_init = State()
    waiting_for_start = State()
    waiting_for_type = State()
    waiting_for_district = State()
    waiting_for_period = State()
    waiting_for_price = State()
    waiting_for_rooms = State()
    waiting_for_condition = State()
    waiting_for_baxi = State()
    waiting_for_conditioner = State()
    waiting_for_home_pets = State()
    waiting_for_pros = State()
    waiting_for_number = State()
    waiting_for_name = State()
    waiting_for_photo = State()
    waiting_for_add_photo = State()
    waiting_for_approve = State()
    waiting_for_edit = State()
    final_state = State()

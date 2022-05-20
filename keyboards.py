from aiogram import types

init_keyboard = types.InlineKeyboardMarkup()
init_keyboard.add(
    types.InlineKeyboardButton(text="Приступим!", callback_data="init")
)

start_keyboard = types.InlineKeyboardMarkup()
buttons = [
    types.InlineKeyboardButton(
        text="Я сдаю свое жилье", callback_data="start_owner"
    ),
    types.InlineKeyboardButton(
        text="Я риэлтор", callback_data="start_realtor"
    ),
]
start_keyboard.add(*buttons)


type_of_house = types.InlineKeyboardMarkup()
buttons = [
    types.InlineKeyboardButton(text="Комната", callback_data="type_room"),
    types.InlineKeyboardButton(
        text="Квартира", callback_data="type_apartment"
    ),
    types.InlineKeyboardButton(text="Дом", callback_data="type_house"),
    types.InlineKeyboardButton(text="🠔 Назад", callback_data="type_back"),
]
type_of_house.add(*buttons)

baxi = types.InlineKeyboardMarkup()
buttons = [
    types.InlineKeyboardButton(text="Да", callback_data="baxi_yes"),
    types.InlineKeyboardButton(text="Нет", callback_data="baxi_no"),
]
baxi.add(*buttons)


air_conditioner = types.InlineKeyboardMarkup()
buttons = [
    types.InlineKeyboardButton(text="Да", callback_data="conditioner_yes"),
    types.InlineKeyboardButton(text="Нет", callback_data="conditioner_no"),
]
air_conditioner.add(*buttons)


add_photos = types.InlineKeyboardMarkup()
buttons = [
    types.InlineKeyboardButton(
        text="Добавить фото", callback_data="add_photo"
    ),
    types.InlineKeyboardButton(
        text="Не добавлять фото", callback_data="no_photo"
    ),
]
add_photos.add(*buttons)

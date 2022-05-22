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
    # types.InlineKeyboardButton(text="Назад", callback_data="type_back"),
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

post_keyboard = types.InlineKeyboardMarkup()
buttons = [
    types.InlineKeyboardButton(
        text="Опубликовать!", callback_data="post_publicate"
    ),
    types.InlineKeyboardButton(
        text="Редактировать", callback_data="post_change"
    ),
]
post_keyboard.add(*buttons)

edit_keyboard = types.InlineKeyboardMarkup()
buttons = [
    types.InlineKeyboardButton(text="Имя", callback_data="change_name"),
    types.InlineKeyboardButton(
        text="Собственник/риэлтор", callback_data="change_person"
    ),
    types.InlineKeyboardButton(text="Тип", callback_data="change_type"),
    types.InlineKeyboardButton(text="Район", callback_data="change_district"),
    types.InlineKeyboardButton(
        text="Состояние", callback_data="change_condition"
    ),
    types.InlineKeyboardButton(text="Животные", callback_data="change_pets"),
    types.InlineKeyboardButton(
        text="Комментарий", callback_data="change_pros"
    ),
    types.InlineKeyboardButton(text="Комнаты", callback_data="change_rooms"),
    types.InlineKeyboardButton(
        text="Отопление Baxi", callback_data="change_baxi"
    ),
    types.InlineKeyboardButton(
        text="Кондиционер", callback_data="change_conditioner"
    ),
    types.InlineKeyboardButton(text="Период", callback_data="change_period"),
    types.InlineKeyboardButton(text="Стоимость", callback_data="change_price"),
    types.InlineKeyboardButton(text="Контакты", callback_data="change_number"),
    types.InlineKeyboardButton(text="Фото", callback_data="change_photo"),
]
edit_keyboard.add(*buttons)

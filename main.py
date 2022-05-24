import logging
from os import getenv
from sys import exit
from typing import List

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv

import keyboards
import text_messages
from album_middleware import AlbumMiddleware
from states import UserInfo

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot_token = getenv("RENT_BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

admin_id = getenv("ADMIN_ID")

bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(
    "localhost", 6379, db=4, pool_size=10, prefix="rent_bot"
)
dp = Dispatcher(bot, storage=storage)


async def send_media_group(data, call=None, message=None, chat_id=admin_id):
    media_group = types.MediaGroup()
    for i, obj in enumerate(data["album"]):
        file_id = obj.photo[-1].file_id

        try:
            # We can also add a caption to each file by
            # specifying `"caption": "text"`
            media_group.attach(
                {
                    "media": file_id,
                    "type": obj.content_type,
                    "caption": text_messages.result_message(data)
                    if i == 0
                    else "",
                }
            )
        except ValueError:
            return await call.message.answer(
                "This type of album is not supported by aiogram."
            )
    await bot.send_media_group(chat_id=chat_id, media=media_group)


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer(
        text_messages.start_message, reply_markup=keyboards.init_keyboard
    )
    await UserInfo.waiting_for_init.set()


@dp.callback_query_handler(Text("init"), state=UserInfo.waiting_for_init)
async def init(call: types.CallbackQuery):
    await call.message.edit_text(
        "Укажите кто Вы", reply_markup=keyboards.start_keyboard
    )
    await call.answer()
    await UserInfo.waiting_for_start.set()


@dp.callback_query_handler(state=UserInfo.waiting_for_start)
async def realtor_or_usual(call: types.CallbackQuery, state: FSMContext):
    value = call.data.split("_")[1]
    type_of_people = {"owner": "Собственник", "realtor": "Риелтор"}
    await state.update_data(person=type_of_people[value])
    await call.message.edit_text(
        f"Отлично, {call.from_user.first_name}! Теперь укажите тип жилья",
        reply_markup=keyboards.type_of_house,
    )
    await UserInfo.next()


@dp.callback_query_handler(
    Text(startswith="type_"), state=UserInfo.waiting_for_type
)
async def type_of_house(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split("_")[1]
    # if data == "back":
    #     # probably may be a problem if do not reset state data
    #     await call.message.edit_text(
    #         "Укажите кто Вы", reply_markup=keyboards.start_keyboard
    #     )
    #     await UserInfo.waiting_for_start.set()

    house = {"room": "Комната", "apartment": "Квартира", "house": "Дом"}
    await state.update_data(type=house[data])
    await call.message.edit_text(
        text="Введите название района, в котором находится жилье\n\n"
        "Лучше всего уточнить улицу и номер дома"
    )
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_district)
async def district(message: types.Message, state: FSMContext):
    await state.update_data(district=message.text)
    await message.answer("На какой период Вы сдаете жилье?")
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_period)
async def period(message: types.Message, state: FSMContext):
    await state.update_data(period=message.text)
    await message.answer("Введите стоимость квартиры")
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_price)
async def state_of_house(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()

    if data["type"] == "room":
        await state.update_data(rooms=1)
        await message.answer(
            "Опишите состояние жилья:\n"
            "- Какой ремонт?\n"
            "- Какие есть предметы мебели?\n"
            "- Какая есть техника?"
        )
        await UserInfo.waiting_for_condition.set()
    else:
        await message.answer("Введите количество комнат")
        await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_rooms)
async def rooms(message: types.Message, state: FSMContext):
    await state.update_data(rooms=message.text)
    await message.answer(
        "Опишите состояние жилья:\n"
        "- Какой ремонт?\n"
        "- Какие есть предметы мебели?\n"
        "- Какая есть техника?"
    )
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_condition)
async def condition(message: types.Message, state: FSMContext):
    await state.update_data(condition=message.text)
    await message.answer(
        "Есть ли Baxi - индивидуальное отопление?",
        reply_markup=keyboards.baxi,
    )
    await UserInfo.next()


@dp.callback_query_handler(state=UserInfo.waiting_for_baxi)
async def baxi(call: types.CallbackQuery, state: FSMContext):
    baxi = call.data.split("_")[1]
    choice = {"yes": "Да", "no": "Нет"}
    await state.update_data(baxi=choice[baxi])
    await call.message.edit_text(
        "Есть ли кондиционер?", reply_markup=keyboards.air_conditioner
    )
    await UserInfo.next()


@dp.callback_query_handler(state=UserInfo.waiting_for_conditioner)
async def conditioner(call: types.CallbackQuery, state: FSMContext):
    conditioner = call.data.split("_")[1]
    choice = {"yes": "Да", "no": "Нет"}
    await state.update_data(conditioner=choice[conditioner])
    await call.message.edit_text("Животные разрешены? Какие?")
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_home_pets)
async def pets(message: types.Message, state: FSMContext):
    await state.update_data(pets=message.text)
    await message.answer("Опишите Ваше жилье")
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_pros)
async def pros(message: types.Message, state: FSMContext):
    await state.update_data(pros=message.text)
    await message.answer(
        "Отлично, мы почти закончили!\n"
        "Оставьте Ваш контактный телефон и/или телеграм"
    )
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_number)
async def phone(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    await message.answer("Как к Вам обращаться?")
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_name)
async def user_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)

    await message.answer(
        "<b>Чтобы Ваше объявление было более заметным, "
        "добавьте фотографии жилья</b>",
        reply_markup=keyboards.add_photos,
    )
    await UserInfo.next()


@dp.callback_query_handler(
    Text(endswith="_photo"), state=UserInfo.waiting_for_photo
)
async def photo_instruction(call: types.CallbackQuery, state: FSMContext):
    action = call.data.split("_")[0]
    if action == "add":
        example = open("./bin/attach_photo.jpg", "rb")
        await bot.send_photo(
            call.from_user.id,
            example,
            caption="Прикрепите фотографии Вашего жилья как "
            "показано в примере",
        )
        example.close()
        await UserInfo.next()
    else:
        data = await state.get_data()
        await call.message.edit_text(text_messages.result_message(data))
        await call.message.answer(
            "Перед публикацией Вы можете отредактировать пост",
            reply_markup=keyboards.post_keyboard,
        )

        await UserInfo.waiting_for_approve.set()


@dp.message_handler(
    is_media_group=True,
    content_types=types.ContentType.PHOTO,
    state=UserInfo.waiting_for_add_photo,
)
async def handle_albums(
    message: types.Message, album: List[types.Message], state: FSMContext
):
    """This handler will receive a complete album of any type."""

    await state.update_data(album=album)
    data = await state.get_data()

    await send_media_group(data, message=message, chat_id=message.chat.id)

    await message.answer(
        "Перед публикацией Вы можете отредактировать пост",
        reply_markup=keyboards.post_keyboard,
    )

    await UserInfo.next()


@dp.message_handler(
    content_types=types.ContentType.PHOTO, state=UserInfo.waiting_for_add_photo
)
async def adding_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(photo=photo)
    data = await state.get_data()

    await bot.send_photo(
        message.from_user.id,
        photo=photo,
        caption=text_messages.result_message(data),
    )
    await message.answer(
        "Перед публикацией Вы можете отредактировать пост",
        reply_markup=keyboards.post_keyboard,
    )

    await UserInfo.next()


@dp.callback_query_handler(state=UserInfo.waiting_for_approve)
async def pub_or_change(call: types.CallbackQuery, state: FSMContext):
    command = call.data.split("_")[1]
    data = await state.get_data()
    if command == "publicate":
        if "data_to_update" in data:
            update_field = data["data_to_update"]
            await state.update_data(data={update_field: call.message.text})
        await call.message.edit_text(
            "Спасибо, Ваше объявление будет опубликовано в канале после "
            "модерации"
        )

        if "album" in data:
            await send_media_group(data, call=call, chat_id=admin_id)

        elif "photo" in data:
            await bot.send_photo(
                chat_id=admin_id,
                photo=data["photo"],
                caption=text_messages.result_message(data),
            )
        else:
            await bot.send_message(
                chat_id=admin_id, text=text_messages.result_message(data)
            )
        await state.finish()
    else:
        await call.message.edit_text(
            "Выберите пункт, который хотите изменить",
            reply_markup=keyboards.edit_keyboard,
        )
        await UserInfo.next()


# fork of possible changes
@dp.callback_query_handler(
    Text(startswith="change_"), state=UserInfo.waiting_for_edit
)
async def change(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split("_")[1]
    if data == "name":
        await call.message.edit_text("Как к Вам обращаться?")
    elif data == "person":
        await call.message.edit_text(
            "Укажите кто Вы", reply_markup=keyboards.start_keyboard
        )
    elif data == "type":
        await call.message.edit_text(
            "Укажите тип жилья", reply_markup=keyboards.type_of_house
        )
    elif data == "district":
        await call.message.edit_text(
            text="Введите название района, в котором находится жилье\n\n"
            "Лучше всего уточнить улицу и номер дома"
        )
    elif data == "condition":
        await call.message.edit_text(
            "Опишите состояние жилья:\n"
            "- Какой ремонт?\n"
            "- Какие есть предметы мебели?\n"
            "- Какая есть техника?"
        )
    elif data == "pets":
        await call.message.edit_text("Животные разрешены? Какие?")

    elif data == "pros":
        await call.message.edit_text("Опишите Ваше жилье")
    elif data == "rooms":
        await call.message.edit_text("Введите количество комнат")
    elif data == "baxi":
        await call.message.edit_text(
            "Есть ли Baxi - индивидуальное отопление?",
            reply_markup=keyboards.baxi,
        )
    elif data == "conditioner":
        await call.message.edit_text(
            "Есть ли кондиционер?", reply_markup=keyboards.air_conditioner
        )
    elif data == "period":
        await call.message.edit_text("На какой период Вы сдаете жилье?")
    elif data == "price":
        await call.message.edit_text("Введите стоимость квартиры")
    elif data == "number":
        await call.message.edit_text(
            "Оставьте Ваш контактный телефон и/или телеграм"
        )
    elif data == "photo":
        await call.message.answer(
            "<b>Чтобы Ваше объявление было более заметным, "
            "добавьте фотографии жилья</b>",
            reply_markup=keyboards.add_photos,
        )
        await UserInfo.waiting_for_photo.set()
        await state.update_data(data_to_update=data)
        return

    await state.update_data(data_to_update=data)
    await UserInfo.next()


# handle changes by message
@dp.message_handler(state=UserInfo.final_state)
async def updating_data(message: types.Message, state: FSMContext):
    data = await state.get_data()
    update_field = data["data_to_update"]
    await state.update_data(data={update_field: message.text})

    data = await state.get_data()
    # we send the user the modified post with the media, if there is one
    if "album" in data:
        await send_media_group(
            data=data, message=message, chat_id=message.chat.id
        )
    elif "photo" in data:
        await bot.send_photo(
            chat_id=admin_id,
            photo=data["photo"],
            caption=text_messages.result_message(data),
        )
    else:
        await message.answer(text_messages.result_message(data))
    await UserInfo.waiting_for_approve.set()
    await message.answer(
        "Перед публикацией Вы можете отредактировать пост",
        reply_markup=keyboards.post_keyboard,
    )


# handle changes by callback from buttons
@dp.callback_query_handler(state=UserInfo.final_state)
async def updating_buttons(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    update_field = data["data_to_update"]
    if update_field in ["baxi", "conditioner"]:
        value = call.data.split("_")[1]
        choice = {"yes": "Да", "no": "Нет"}
        await state.update_data(data={update_field: choice[value]})

    elif update_field == "type":
        value = call.data.split("_")[1]
        house = {"room": "Комната", "apartment": "Квартира", "house": "Дом"}
        await state.update_data(data={update_field: house[value]})

    elif update_field == "person":
        value = call.data.split("_")[1]
        type_of_people = {"owner": "Собственник", "realtor": "Риелтор"}
        await state.update_data(data={update_field: type_of_people[value]})

    data = await state.get_data()
    await call.message.answer(text_messages.result_message(data))
    await UserInfo.waiting_for_approve.set()
    await call.message.answer(
        "Перед публикацией Вы можете отредактировать пост",
        reply_markup=keyboards.post_keyboard,
    )


async def on_shutdown(dp):
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == "__main__":
    dp.middleware.setup(AlbumMiddleware())
    executor.start_polling(dp, skip_updates=True, on_shutdown=on_shutdown)

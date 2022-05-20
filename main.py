import logging
from os import getenv
from sys import exit
from typing import List

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
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
dp = Dispatcher(bot, storage=MemoryStorage())


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
    await call.message.answer(
        "Укажите кто Вы", reply_markup=keyboards.start_keyboard
    )
    await call.answer()
    await UserInfo.waiting_for_start.set()


@dp.callback_query_handler(state=UserInfo.waiting_for_start)
async def realtor_or_usual(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(person=call.data.split("_")[1])
    await call.message.edit_text(
        f"Отлично, {call.from_user.first_name}, теперь укажите тип жилья",
        reply_markup=keyboards.type_of_house,
    )
    await UserInfo.next()


@dp.callback_query_handler(
    Text(startswith="type_"), state=UserInfo.waiting_for_type
)
async def type_of_house(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split("_")[1]
    if data == "back":
        # probably may be a problem if do not reset state data
        await call.message.edit_text(
            "Укажите кто Вы", reply_markup=keyboards.start_keyboard
        )
        await UserInfo.waiting_for_start.set()
    else:
        house = {"room": "комната", "apartment": "квартира", "house": "дом"}
        await state.update_data(type=house[data])
        await call.message.edit_text(
            text="Введите название района, в котором находится жилье"
        )
        await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_district)
async def district(message: types.Message, state: FSMContext):
    await state.update_data(district=message.text.lower())
    await message.answer("На какой период Вы сдаете жилье?")
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_period)
async def period(message: types.Message, state: FSMContext):
    await state.update_data(period=message.text.lower())
    await message.answer("Введите стоимость квартиры")
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_price)
async def state_of_house(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text.lower())
    data = await state.get_data()

    if data["type"] == "room":
        await state.update_data(rooms=1)
        await message.answer(
            "Состояние квартиры:\n"
            "- Какой ремонт?\n"
            "- Какие предметы мебели есть?"
        )
        await UserInfo.waiting_for_condition.set()
    else:
        await message.answer("Введите количество комнат")
        await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_rooms)
async def rooms(message: types.Message, state: FSMContext):
    await state.update_data(rooms=message.text.lower())
    await message.answer(
        "Состояние квартиры:\n"
        "- Какой ремонт?\n"
        "- Какие предметы мебели есть?"
    )
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_condition)
async def condition(message: types.Message, state: FSMContext):
    await state.update_data(condition=message.text.lower())
    await message.answer("Есть ли в квартире Baxi - индивидуальное отопление?")
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_baxi)
async def baxi(message: types.Message, state: FSMContext):
    await state.update_data(baxi=message.text.lower())
    await message.answer("Есть ли кондиционер?")
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_conditioner)
async def conditioner(message: types.Message, state: FSMContext):
    await state.update_data(conditioner=message.text.lower())
    await message.answer("Животные разрешены?")
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_home_pets)
async def pets(message: types.Message, state: FSMContext):
    await state.update_data(pets=message.text.lower())
    await message.answer("Опишите Вашу квартиру")
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_pros)
async def pros(message: types.Message, state: FSMContext):
    await state.update_data(pros=message.text.lower())
    await message.answer(
        "Отлично, мы почти закончили!\nОставьте Ваш контактный номер телефона"
    )
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_number)
async def phone(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text.lower())
    await message.answer("Как к Вам обращаться?")
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_name)
async def user_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.lower())
    # data = await state.get_data()
    await message.answer(
        "<b>Чтобы Ваше объявление было в приоритете поиска, "
        "добавьте несколько фотографий жилья</b>",
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
        await call.message.answer(
            "Прикрепите фотографии Вашего жилья как показано в примере"
        )
        await bot.send_photo(call.from_user.id, example)
        example.close()
        await UserInfo.next()
    else:
        data = await state.get_data()
        await call.message.edit_text(text_messages.result_message(data))
        await bot.send_message(
            chat_id=admin_id, text=text_messages.result_message(data)
        )
        await state.finish()


@dp.message_handler(
    is_media_group=True,
    content_types=types.ContentType.PHOTO,
    state=UserInfo.waiting_for_add_photo,
)
async def handle_albums(
    message: types.Message, album: List[types.Message], state: FSMContext
):
    """This handler will receive a complete album of any type."""
    media_group = types.MediaGroup()
    data = await state.get_data()
    for i, obj in enumerate(album):
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
            return await message.answer(
                "This type of album is not supported by aiogram."
            )

    # await message.answer(text_messages.result_message(data))
    await message.answer_media_group(media_group)
    await bot.send_media_group(chat_id=admin_id, media=media_group)

    await state.finish()


@dp.message_handler(
    content_types=types.ContentType.PHOTO, state=UserInfo.waiting_for_add_photo
)
async def adding_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()

    await bot.send_photo(
        message.from_user.id,
        photo=photo,
        caption=text_messages.result_message(data),
    )
    await bot.send_photo(
        chat_id=admin_id,
        photo=photo,
        caption=text_messages.result_message(data),
    )
    await state.finish()


if __name__ == "__main__":
    dp.middleware.setup(AlbumMiddleware())
    executor.start_polling(dp, skip_updates=True)

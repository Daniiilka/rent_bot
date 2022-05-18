import logging
from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from sys import exit

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

import text_messages, keyboards
from states import UserInfo


logging.basicConfig(level=logging.INFO)

bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.answer(text_messages.start_message, reply_markup=keyboards.init_keyboard)
    await UserInfo.waiting_for_init.set()


@dp.callback_query_handler(Text('init'), state=UserInfo.waiting_for_init)
async def init(call: types.CallbackQuery):
    await call.message.answer('Укажите кто Вы', reply_markup=keyboards.start_keyboard)
    await UserInfo.waiting_for_start.set()


@dp.callback_query_handler(state=UserInfo.waiting_for_start)
async def realtor_or_usual(call: types.CallbackQuery, state: FSMContext):

    await state.update_data(person=call.data.split('_')[1])
    # user = await state.get_data()
    # await call.answer(text=user['realtor'])

    await call.message.edit_text(f'Отлично, {call.from_user.first_name}, теперь укажите тип жилья',
                                 reply_markup=keyboards.type_of_house)
    await UserInfo.next()


@dp.callback_query_handler(Text(startswith='type_'), state=UserInfo.waiting_for_type)
async def type_of_house(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split('_')[1]
    if data == 'back':
        await UserInfo.waiting_for_init.set()

    await state.update_data(type=call.data.split('_')[1])





# @dp.message_handler(commands="special_buttons")
# async def cmd_special_buttons(message: types.Message):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(types.KeyboardButton(text="Запросить геолокацию", request_location=True))
#     keyboard.add(types.KeyboardButton(text="Запросить контакт", request_contact=True))
#     keyboard.add(types.KeyboardButton(text="Создать викторину",
#                                       request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)))
#     await message.answer("Выберите действие:", reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
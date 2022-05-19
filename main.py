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
    await call.answer(text='⚡')
    await UserInfo.waiting_for_start.set()


@dp.callback_query_handler(state=UserInfo.waiting_for_start)
async def realtor_or_usual(call: types.CallbackQuery, state: FSMContext):

    await state.update_data(person=call.data.split('_')[1])
    await call.message.edit_text(f'Отлично, {call.from_user.first_name}, '
                                 f'теперь укажите тип жилья',
                                 reply_markup=keyboards.type_of_house)
    await UserInfo.next()


@dp.callback_query_handler(Text(startswith='type_'), state=UserInfo.waiting_for_type)
async def type_of_house(call: types.CallbackQuery, state: FSMContext):
    data = call.data.split('_')[1]
    if data == 'back':
        # probably may be a problem if do not reset state data
        await call.message.edit_text('Укажите кто Вы', reply_markup=keyboards.start_keyboard)
        await UserInfo.waiting_for_start.set()
    else:
        await state.update_data(type=call.data.split('_')[1])
        await call.message.edit_text(text='Введите название района, в котором находится жилье')
        await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_district)
async def district(message: types.Message, state: FSMContext):
    await state.update_data(district=message.text.lower())
    await message.answer('На какой период Вы сдаете жилье?')
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_period)
async def period(message: types.Message, state: FSMContext):
    await state.update_data(period=message.text.lower())
    await message.answer('Введите стоимость квартиры')
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_price)
async def type_of_house(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text.lower())
    data = await state.get_data()

    if data['type'] == 'room':
        await state.update_data(rooms=1)
        await message.answer('Состояние квартиры:\n1. Какой ремонт?\n2. Какие есть предметы мебели?')
        await UserInfo.waiting_for_condition.set()
    else:
        await message.answer('Введите количество комнат')
        await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_rooms)
async def rooms(message: types.Message, state: FSMContext):
    await state.update_data(rooms=message.text.lower())
    await message.answer('Состояние квартиры:\n1. Какой ремонт?\n2. Какие есть предметы мебели?')
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_condition)
async def condition(message: types.Message, state: FSMContext):
    await state.update_data(condition=message.text.lower())
    await message.answer('Есть ли в квартире Baxi - индивидуальное отопление?')
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_baxi)
async def baxi(message: types.Message, state: FSMContext):
    await state.update_data(baxi=message.text.lower())
    await message.answer('Есть ли кондиционер?')
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_conditioner)
async def baxi(message: types.Message, state: FSMContext):
    await state.update_data(conditioner=message.text.lower())
    await message.answer('Животные разрешены?')
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_home_pets)
async def pets(message: types.Message, state: FSMContext):
    await state.update_data(pets=message.text.lower())
    await message.answer('Опишите Вашу квартиру')
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_pros)
async def pros(message: types.Message, state: FSMContext):
    await state.update_data(pros=message.text.lower())
    await message.answer('Отлично, мы почти закончили!\nОставьте Ваш контактный номер телефона')
    await UserInfo.next()


@dp.message_handler(state=UserInfo.waiting_for_number)
async def pros(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text.lower())
    data = await state.get_data()
    await message.answer('Поздравляем!\nВаше объявление будет иметь следующий вид:\n'
                         f'Меня зовут: {message.from_user.first_name}\n'
                        f'Тип Жилья: {data["type"]}\n'
                         f'Район: {data["district"]}\n'
                         f'Состояние квартиры: {data["condition"]}')

# 'Отношение к животным: да'
#
# 'Комментарий от владельца: все'
#
# 'Количество комнат: 3'
#
# 'Наличие отопления (Baxi): Да'
#
# 'Наличие кондиционера: Да'
#
# 'Сдаю на период: на два дня'
#
#
# 'Стоимость в месяц: мильон '
#
# 'Контактный телефон:')"'






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
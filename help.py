import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import IDFilter, IsReplyFilter, Text
from aiogram.types import ContentType, Message

import keyboards
from keyboards import support_markup
from loader import admin_id, dp
from states import SupportStates

logger = logging.getLogger(__name__)


@dp.callback_query_handler(Text("help"))
async def ask_support(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(
        "Напишите текстом ваш вопрос и мы ответим в ближайшее время!",
        reply_markup=support_markup,
    )
    await call.answer()
    await SupportStates.asking.set()
    await state.update_data(support_message_count=0)


@dp.message_handler(
    Text(equals="Вопрос решен!"),
    state=SupportStates.asking,
    content_types=ContentType.TEXT,
)
async def support_requested_finish(message: Message, state: FSMContext):
    data = await state.get_data()
    logger.info(
        f"request closed: {message.from_user.id} "
        f"{message.from_user.full_name} "
        f"(@{message.from_user.username}) via "
        f"{data['support_message_count']} messages"
    )
    # for admin in config.ADMINS:
    #     await dp.bot.send_message(
    #         admin,
    #         f"{message.from_user.id}\n"
    #         f"{message.text}\n"
    #         f"Количество сообщений: {data['support_message_count']}",
    #         disable_notification=True,
    #     )
    #
    await message.answer(
        "Рады помочь!", reply_markup=keyboards.continue_keyboard
    )
    await state.finish()


@dp.message_handler(state=SupportStates.asking, content_types=ContentType.TEXT)
async def support_requested(message: Message, state: FSMContext):

    await dp.bot.send_message(
        admin_id,
        f"{message.from_user.id}\n"
        f"{message.from_user.full_name} (@{message.from_user.username})\n"
        f"{message.text}",
    )
    data = await state.get_data()
    if data["support_message_count"] == 0:
        await message.answer("Сообщение отправлено администратору!")
    await state.update_data(
        support_message_count=data["support_message_count"] + 1
    )


@dp.message_handler(IsReplyFilter(True), IDFilter(chat_id=admin_id))
async def reply_support(message: Message, state: FSMContext):
    to = message.reply_to_message.text.split("\n")[0]
    current_state = await state.get_state()
    if current_state == SupportStates.asking:
        await dp.bot.send_message(
            to, message.text, reply_markup=support_markup
        )
    else:
        await dp.bot.send_message(to, message.text)
    await message.reply_to_message.edit_text(
        f"{message.reply_to_message.text}\n-> {message.text}"
    )
    await message.delete()

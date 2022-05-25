import logging
from os import getenv
from sys import exit

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot_token = getenv("RENT_BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

admin_id = getenv("ADMIN_ID")

bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
# storage = RedisStorage2(
#     "localhost", 6379, db=4, pool_size=10, prefix="rent_bot"
# )
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

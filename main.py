import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

TOKEN = "6453190990:AAHl0KKebb_XWxZBtTa_rAwDXTIkHrudFrg"


async def get_start(message: Message, bot: Bot):
    await bot.send_message(message.from_user.id,
                           f"")


# Запуск бота
async def start():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()


# Проверка на файл
if __name__ == "__main__":
    asyncio.run(start())
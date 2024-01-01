import asyncio
import logging
import sys
import os
import dotenv

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hitalic

from keyboards.reply import greeting_keyboard, price_keyboard, oplata_keyboard_1_month, oplata_keyboard_2_month, \
    oplata_keyboard_3_month
from data.config import price_list, dostup_text, pic
from handlers import callbacks
from utils.statesform import GetWalletForm


dotenv.load_dotenv(dotenv.find_dotenv())

bot = Bot(os.getenv('TG_TOKEN'))
dp = Dispatcher()


# Начальная фраза
@dp.message(CommandStart())
async def get_start(message: Message, bot: Bot):
    await message.answer(hbold("Привет,", message.from_user.username) + "!\n\n"
                         f"С помощью этого бота ты сможешь купить доступ в мою приватку.\n\n"
                         f"{hitalic('Для помощи напиши /help')}\n\n"
                         f"{hbold(f'АДМИН: @tyoma5e')}",
                         parse_mode=ParseMode.HTML,
                         reply_markup=greeting_keyboard)


# Кнопка покупки подписки
@dp.message(F.text == "Получить доступ 📈")
async def dostup(message: Message, bot: Bot):
    await message.answer(hbold("Выберите интересующий вас период:"),
                         parse_mode=ParseMode.HTML,
                         reply_markup=price_keyboard)


# Кнопка 1 месяц
@dp.message(F.text == "Доступ на 1 месяц 👶")
async def one_month(message: Message, bot: Bot):
    text = dostup_text.substitute(price=price_list[0])
    await bot.send_photo(message.from_user.id,
                         photo=pic,
                         caption=text,
                         parse_mode=ParseMode.HTML,
                         reply_markup=oplata_keyboard_1_month
                         )


# Кнопка 1 месяц
@dp.message(F.text == "Доступ на 2 месяца 🤩")
async def two_months(message: Message, bot: Bot):
    text = dostup_text.substitute(price=price_list[1])
    await bot.send_photo(message.from_user.id,
                         photo=pic,
                         caption=text,
                         parse_mode=ParseMode.HTML,
                         reply_markup=oplata_keyboard_2_month
                         )


# Кнопка 1 месяц
@dp.message(F.text == "Доступ на 3 месяца 👑")
async def three_months(message: Message, bot: Bot):
    text = dostup_text.substitute(price=price_list[2])
    await bot.send_photo(message.from_user.id,
                         photo=pic,
                         caption=text,
                         parse_mode=ParseMode.HTML,
                         reply_markup=oplata_keyboard_3_month
                         )


# Кнопка назад в меню
@dp.message(F.text == "Назад")
async def get_start(message: Message, bot: Bot):
    await message.answer(hbold('Вы вернулись в меню↩️'),
                         parse_mode=ParseMode.HTML,
                         reply_markup=greeting_keyboard)


# Обработка коллбека оплаты 1 месяца
dp.callback_query.register(callbacks.predup_form, F.data.startswith("oplata"))
dp.message.register(callbacks.get_wallet, GetWalletForm.GET_WALLET)


# Запуск бота
async def start():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


# Проверка на файл
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())
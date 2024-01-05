import asyncio
import logging
import sys
import os
import dotenv
import sqlite3
import requests
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hitalic

from keyboards.reply import greeting_keyboard, price_keyboard, oplata_keyboard_1_month, oplata_keyboard_2_month, \
    oplata_keyboard_3_month
from data.config import price_list, dostup_text, pic, problem, success, uncorrect_summ
from handlers import callbacks
from utils.statesform import GetWalletForm1, GetWalletForm2, GetWalletForm3

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
async def back(message: Message, bot: Bot):
    await message.answer(hbold('Вы вернулись в меню↩️'),
                         parse_mode=ParseMode.HTML,
                         reply_markup=greeting_keyboard)


# Кнопка отмены
@dp.message(F.text == "Отмена ❌")
async def cansel(message: Message, bot: Bot):
    await message.answer(hbold('Выберите интересующий вас период:'),
                         parse_mode=ParseMode.HTML,
                         reply_markup=price_keyboard)


# Кнопка подтверждения перевода 1 месяца
@dp.message(F.text == "Подвердить перевод 💵")
async def confirm(message: Message):
    await tranzaction_info(message, 1)


# Кнопка подтверждения перевода 2 месяца
@dp.message(F.text == "Подвердить перевод 💰")
async def confirm(message: Message):
    await tranzaction_info(message, 2)


# Кнопка подтверждения перевода 3 месяца
@dp.message(F.text == "Подвердить перевод 👑")
async def confirm(message: Message):
    await tranzaction_info(message, 3)


# Вспомогательная функция
async def tranzaction_info(message: Message, month):
    # Подключение к бд
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()
    user_wallet = cursor.execute(f"SELECT wallet FROM users WHERE username='{message.from_user.username}'").fetchone()[
        0]
    # Получение информации о транзах с кошелька пользователя
    r_link = f"https://api.trongrid.io/v1/accounts/{user_wallet}/transactions/trc20"
    data = requests.get(r_link, params={'limit': 3}, headers={"accept": "application/json"}).json()

    # Проход по транзам и получение нужной
    for tr in data.get('data', []):
        symbol = tr.get('token_info', {}).get('symbol')
        to = tr.get('to')
        v = tr.get('value', '')

        dec = -1 * int(tr.get('token_info', {}).get('decimals', '6'))
        f = float(v[:dec] + '.' + v[dec:])

        if symbol == "USDT":
            if month == 1:
                if 34 < f < 36:
                    link = await bot.create_chat_invite_link(chat_id=os.getenv("CHAT_ID"), member_limit=1)
                    await message.answer(success.substitute(link=link.invite_link), parse_mode=ParseMode.HTML)
                else:
                    text = uncorrect_summ.substitute(summ=hbold(str(f) + " USDT"))
                    await message.answer(text,
                                         parse_mode=ParseMode.HTML)
            elif month == 2:
                if 69 < f < 71:
                    link = await bot.create_chat_invite_link(chat_id=os.getenv("CHAT_ID"), member_limit=1)
                    await message.answer(success.substitute(link=link.invite_link), parse_mode=ParseMode.HTML)
                else:
                    text = uncorrect_summ.substitute(summ=hbold(str(f) + " USDT"))
                    await message.answer(text,
                                         parse_mode=ParseMode.HTML)
            else:
                if 99 < f < 101:
                    link = await bot.create_chat_invite_link(chat_id=os.getenv("CHAT_ID"), member_limit=1)
                    await message.answer(success.substitute(link=link.invite_link), parse_mode=ParseMode.HTML)
                else:
                    text = uncorrect_summ.substitute(summ=hbold(str(f) + " USDT"))
                    await message.answer(text,
                                         parse_mode=ParseMode.HTML)
        else:
            await message.answer(problem)


# Обработка коллбека оплаты 1 месяца
dp.callback_query.register(callbacks.predup_form1, F.data == "oplata1")
dp.message.register(callbacks.get_wallet1, GetWalletForm1.GET_WALLET)
# Обработка коллбека оплаты 2 месяца
dp.callback_query.register(callbacks.predup_form2, F.data == "oplata2")
dp.message.register(callbacks.get_wallet2, GetWalletForm2.GET_WALLET)
# Обработка коллбека оплаты 3 месяца
dp.callback_query.register(callbacks.predup_form3, F.data == "oplata3")
dp.message.register(callbacks.get_wallet3, GetWalletForm3.GET_WALLET)


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
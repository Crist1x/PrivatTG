from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram import Bot, F
from data.config import predup_text, oplata_text, price_list
from utils.statesform import GetWalletForm1, GetWalletForm2, GetWalletForm3
from keyboards.reply import confirmation_kb1, confirmation_kb2, confirmation_kb3

import dotenv
import os
import requests
import sqlite3

dotenv.load_dotenv(dotenv.find_dotenv())
bot = Bot(os.getenv("TG_TOKEN"))


# Колбек предупрждения 1 месяц
async def predup_form1(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id,
                           predup_text,
                           parse_mode=ParseMode.HTML)

    await state.set_state(GetWalletForm1.GET_WALLET)


# 2 месяца
async def predup_form2(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id,
                           predup_text,
                           parse_mode=ParseMode.HTML)

    await state.set_state(GetWalletForm2.GET_WALLET)


# 3 месяца
async def predup_form3(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id,
                           predup_text,
                           parse_mode=ParseMode.HTML)

    await state.set_state(GetWalletForm3.GET_WALLET)


# Функция получения кошелька для 1 месяца
async def get_wallet1(message: Message, state: FSMContext):
    # проверка кошелька на валидность
    wallet_check = requests.get(f"https://api.trongrid.io/v1/accounts/{message.text}/transactions/trc20",
                                headers={"accept": "application/json"}).json()
    # если не успешно
    if not wallet_check["success"]:
        await message.answer("Такого кошелька не существует. Повторите попытку ввода: ")
        await state.clear()
        await state.set_state(GetWalletForm1.GET_WALLET)

    # если успешно
    else:
        await wallet_append(message, state, 0)


# Функция получения кошелька для 2 месяца
async def get_wallet2(message: Message, state: FSMContext):
    # проверка кошелька на валидность
    wallet_check = requests.get(f"https://api.trongrid.io/v1/accounts/{message.text}/transactions/trc20",
                                headers={"accept": "application/json"}).json()
    # если не успешно
    if not wallet_check["success"]:
        await message.answer("Такого кошелька не существует. Повторите попытку ввода: ")
        await state.clear()
        await state.set_state(GetWalletForm2.GET_WALLET)

    # если успешно
    else:
        await wallet_append(message, state, 1)


# Функция получения кошелька для 3 месяца
async def get_wallet3(message: Message, state: FSMContext):
    # проверка кошелька на валидность
    wallet_check = requests.get(f"https://api.trongrid.io/v1/accounts/{message.text}/transactions/trc20",
                                headers={"accept": "application/json"}).json()
    # если не успешно
    if not wallet_check["success"]:
        await message.answer("Такого кошелька не существует. Повторите попытку ввода: ")
        await state.clear()
        await state.set_state(GetWalletForm3.GET_WALLET)

    # если успешно
    else:
        await wallet_append(message, state, 2)


async def wallet_append(message: Message, state: FSMContext, month):
    await state.update_data(wallet=message.text)
    connection = sqlite3.connect('db/database.db')
    cursor = connection.cursor()

    not_first_time = cursor.execute("SELECT username FROM users WHERE username=?",
                                    (message.from_user.username,)).fetchone()
    wallet_num = await state.get_data()

    if not_first_time:
        cursor.execute(
            f"UPDATE users SET wallet = '{wallet_num.get('wallet')}' WHERE username = '{message.from_user.username}'")
    else:
        cursor.execute(f"""INSERT INTO users
                                          (username, wallet, date_start, date_finish)
                                          VALUES
                                          ('{message.from_user.username}', '{wallet_num.get('wallet')}', '', '');""")
    connection.commit()
    cursor.close()
    await message.answer("Кошелек получен✅")
    await state.clear()
    text = oplata_text.substitute(price=price_list[month])
    if month == 0:
        await message.answer(text=text,
                             parse_mode=ParseMode.HTML,
                             reply_markup=confirmation_kb1)
    elif month == 1:
        await message.answer(text=text,
                             parse_mode=ParseMode.HTML,
                             reply_markup=confirmation_kb2)
    else:
        await message.answer(text=text,
                             parse_mode=ParseMode.HTML,
                             reply_markup=confirmation_kb3)
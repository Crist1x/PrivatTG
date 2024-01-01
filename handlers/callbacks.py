from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram import Bot, F
from data.config import predup_text
from utils.statesform import GetWalletForm

import dotenv
import os
import requests
import sqlite3

dotenv.load_dotenv(dotenv.find_dotenv())
bot = Bot(os.getenv("TG_TOKEN"))


# Колбек предупрждения
async def predup_form(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id,
                           predup_text,
                           parse_mode=ParseMode.HTML)
    await state.set_state(GetWalletForm.GET_WALLET)


# Функция получения кошелька
async def get_wallet(message: Message, state: FSMContext):
    # проверка кошелька на валидность
    wallet_check = requests.get(f"https://api.trongrid.io/v1/accounts/{message.text}/transactions/trc20",
                     headers={"accept": "application/json"}).json()
    print(wallet_check)
    # если не успешно
    if not wallet_check["success"]:
        await message.answer("Такого кошелька не существует. Повторите попытку ввода: ")
        await state.clear()
        await state.set_state(GetWalletForm.GET_WALLET)

    # если успешно
    else:
        await state.update_data(wallet=message.text)
        connection = sqlite3.connect('db/database.db')
        cursor = connection.cursor()

        not_first_time = cursor.execute("SELECT username FROM users WHERE username=?", (message.from_user.username, )).fetchone()
        wallet_num = await state.get_data()

        if not_first_time:
            cursor.execute(f"UPDATE users SET wallet = '{wallet_num.get('wallet')}' WHERE username = '{message.from_user.username}'")
        else:
            cursor.execute(f"""INSERT INTO users
                                      (username, wallet, date_start, date_finish)
                                      VALUES
                                      ('{message.from_user.username}', '{wallet_num.get('wallet')}', '', '');""")
        connection.commit()
        cursor.close()
        await message.answer("Кошелек получен✅")
        await state.clear()

        # Распрделение периодов
        if F.data == "oplata1":
            pass





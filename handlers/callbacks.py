from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram import Bot
from data.config import oplata_text
from utils.statesform import Oplata1Form

import dotenv
import os
import requests

dotenv.load_dotenv(dotenv.find_dotenv())
bot = Bot(os.getenv("TG_TOKEN"))


# Колбек оплаты 1 месяца
async def oplata1_form(message: Message, state: FSMContext):
    await bot.send_message(message.from_user.id,
                           oplata_text,
                           parse_mode=ParseMode.HTML)
    await state.set_state(Oplata1Form.GET_WALLET)


async def get_wallet(message: Message):
    # TODO: Сдеать проверку существует ли кошелек или нет и добавить пользователя в бд, если есть
    r = requests.get(f"https://api.trongrid.io/v1/accounts/{str(os.getenv('TYOMA_WALLET'))}/transactions/trc20",
                     headers={"accept": "application/json"})
    print(r.json())
    await message.answer("Кошелек получен.")


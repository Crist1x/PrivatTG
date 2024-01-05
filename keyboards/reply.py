from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

greeting_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Получить доступ 📈")
    ]
], resize_keyboard=True)

price_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Доступ на 1 месяц 👶"),
        KeyboardButton(text="Доступ на 2 месяца 🤩")
    ],
    [
        KeyboardButton(text="Доступ на 3 месяца 👑")
    ],
    [
        KeyboardButton(text="Назад")
    ]
], resize_keyboard=True)


oplata_keyboard_1_month = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Оплатить месяц",
            callback_data="oplata1"
        )
    ]
], resize_keyboard=True)

oplata_keyboard_2_month = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Оплатить 2 месяца",
            callback_data="oplata2"
        )
    ]
], resize_keyboard=True)

oplata_keyboard_3_month = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Оплатить 3 месяца",
            callback_data="oplata3"
        )
    ]
], resize_keyboard=True)

confirmation_kb1 = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Подвердить перевод 💵")
    ],
    [
        KeyboardButton(text="Отмена ❌")
    ]
], resize_keyboard=True)

confirmation_kb2 = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Подвердить перевод 💰")
    ],
    [
        KeyboardButton(text="Отмена ❌")
    ]
], resize_keyboard=True)

confirmation_kb3 = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Подвердить перевод 👑")
    ],
    [
        KeyboardButton(text="Отмена ❌")
    ]
], resize_keyboard=True)

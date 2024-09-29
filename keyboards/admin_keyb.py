from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

access = ReplyKeyboardMarkup(resize_keyboard=True)
access.add(
    KeyboardButton("Дать доступ"),
    KeyboardButton("Не дать доступ")
)

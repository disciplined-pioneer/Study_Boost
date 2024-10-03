from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

registration_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Инструкция 📕')],
        [KeyboardButton(text='Регистрация 📝')],
        [KeyboardButton(text='Войти в систему 🚪')],
        [KeyboardButton(text='Создатель ©️')],
        [KeyboardButton(text='Помощь ❓')]
    ],
    resize_keyboard=True  # Сделаем клавиатуру компактной
)

agreement = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Я согласен ✅", callback_data="agreement_users")]
    ])
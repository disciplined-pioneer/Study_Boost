from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

registration_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Инструкция 📕'), KeyboardButton(text='Создатель ©️')],
        [KeyboardButton(text='Оплатить подписку 💳'), KeyboardButton(text='Виды подписок 💵')],
        [KeyboardButton(text='Войти в систему 🚪')]
    ],
    resize_keyboard=True
)

agreement = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Я согласен ✅", callback_data="agreement_users")]
    ])
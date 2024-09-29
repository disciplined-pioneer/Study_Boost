from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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

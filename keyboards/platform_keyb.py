from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

platform_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Кнопка 1')],
        [KeyboardButton(text='Кнопка 2')],
        [KeyboardButton(text='Кнопка 3')]
    ],
    resize_keyboard=True  # Сделаем клавиатуру компактной
)

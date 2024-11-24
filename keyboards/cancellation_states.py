from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

complete_process = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Завершить ✅')],
        [KeyboardButton(text='Отменить ❌')]
    ],
    resize_keyboard=True  # Сделаем клавиатуру компактной
)

cancel_state = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отменить ❌')]
    ],
    resize_keyboard=True  # Сделаем клавиатуру компактной
)
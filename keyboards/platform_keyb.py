from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

platform_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Советы 🦉')],
        [KeyboardButton(text='Материалы 📔')],
        [KeyboardButton(text='Мероприятия 🎉')],
        [KeyboardButton(text='Помощь ❓'), KeyboardButton(text='Предложения ➕')]
    ],
    resize_keyboard=True  # Сделаем клавиатуру компактной
)

adviсe_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Учёба и успеваемость 👨🏻‍🏫')],
        [KeyboardButton(text='Здоровье и благополучие ❤️')],
        [KeyboardButton(text='Социальная жизнь 🧍')],
        [KeyboardButton(text='Работа и карьера 💼')],
        [KeyboardButton(text='Добавить совет ➕'), KeyboardButton(text='Назад 🔙')]
    ],
    resize_keyboard=True  # Сделаем клавиатуру компактной
)

category_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Учёба и успеваемость 👨🏻‍🏫', callback_data='study')],
        [InlineKeyboardButton(text='Здоровье и благополучие ❤️', callback_data='health')],
        [InlineKeyboardButton(text='Социальная жизнь 🧍', callback_data='social')],
        [InlineKeyboardButton(text='Работа и карьера 💼', callback_data='work')]
    ]
)
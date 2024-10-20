from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Обновлённое меню платформы
platform_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Советы 🦉'), KeyboardButton(text='Материалы 📔')],
        [KeyboardButton(text='Мероприятия 🎉')],
        [KeyboardButton(text='Помощь ❓'), KeyboardButton(text='Предложения ➕')]
    ],
    resize_keyboard=True  # Сделаем клавиатуру компактной
)

# Обновлённое меню для советов
advice_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Просмотреть категории 🗂')],
        [KeyboardButton(text='Добавить совет ➕')],
        [KeyboardButton(text='Назад 🔙')]
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

view_category_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Учёба и успеваемость 👨🏻‍🏫', callback_data='view_study')],
        [InlineKeyboardButton(text='Здоровье и благополучие ❤️', callback_data='view_health')],
        [InlineKeyboardButton(text='Социальная жизнь 🧍', callback_data='view_social')],
        [InlineKeyboardButton(text='Работа и карьера 💼', callback_data='view_work')]
    ]
)
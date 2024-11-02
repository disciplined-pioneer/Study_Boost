from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

platform_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Советы 🦉')],
        [KeyboardButton(text='Мероприятия 🎉')],
        [KeyboardButton(text='Материалы 📔')],
        [KeyboardButton(text='Настройки ⚙️')]
    ],
    resize_keyboard=True  # Сделаем клавиатуру компактной
)

settings_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Команды 📜')],
        [KeyboardButton(text='Предложения ➕')],
        [KeyboardButton(text='Помощь ❓')],
        [KeyboardButton(text='Назад 🔙')]
    ],
    resize_keyboard=True  # Сделаем клавиатуру компактной
)

# Меню для советов
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

grade_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='👍', callback_data='like'), InlineKeyboardButton(text='👎', callback_data='dislike')]
    ]
)